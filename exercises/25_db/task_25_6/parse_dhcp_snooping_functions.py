import os
import re
import yaml
import sqlite3
from tabulate import tabulate


YAML_SWITCHES_PATH = "switches.yml"


def create_db(db_file_path, path_to_schema):
    if os.path.isfile(db_file_path):
        pass
    else:
        create_script_str = get_script_from_file(path_to_schema)

        conn = sqlite3.connect(db_file_path)
        with conn:
            print("Создаю базу данных...")
            conn.executescript(create_script_str)
        conn.close()


def get_script_from_file(file_path):
    with open(file_path) as f:
        script = f.read()
    return script


def add_data_switches(db_file, yaml_filename):
    switches_d = {}
    for file in yaml_filename:
        with open(file) as f:
            switches_d.update(yaml.safe_load(f)['switches'])

    query = "INSERT into switches values (?, ?)"
    conn = sqlite3.connect(db_file)
    for row in switches_d.items():
        try:
            with conn:
                conn.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных: {row} Возникла ошибка: {err}")
    conn.close()


def get_text_from_file(file_path):
    with open(file_path) as f:
        script = f.read()
    return script


def get_dhcp_list_from_text(output, device_name):
    regex = re.compile(
        r"\n(?P<mac>\w\w(?::\w\w){5}) +(?P<ip>\d+.\d+.\d+.\d+) +\d+ "
        r"+dhcp-snooping +(?P<vlan>\d+) +(?P<intf>\S+)"
    )
    return [match.groups() + (device_name, ) for match in regex.finditer(output)]


def set_all_dhcp_to_false_activity(db_name):
    query = "UPDATE dhcp set active=0"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except sqlite3.IntegrityError as err:
        print(f"При обнуление статуса ACTIVE возникла ошибка: {err}")
        
    connection.commit()
    connection.close()


def add_data(db_file, file_pathes):
    output = ""
    full_list = []

    for file in file_pathes:
        split_pathes = file.split("/")
        if len(split_pathes) > 1:
            file_name = split_pathes[-1::][0]
        else:
            file_name = file

        device_name = file_name[:file_name.find("_dhcp"):]
        output = get_text_from_file(file)
        full_list.extend(get_dhcp_list_from_text(output, device_name))
    
    set_all_dhcp_to_false_activity(db_file)

    query = "REPLACE into dhcp values (?, ?, ?, ?, ?, 1, datetime('now'))"
    conn = sqlite3.connect(db_file)
    for row in full_list:
        try:
            with conn:
                conn.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных: {row} Возникла ошибка: {err}")
        
    conn.close()


def get_data(db_file, key, value):
    query = f'SELECT * from dhcp WHERE {key}="{value}" AND active = 1'
    output = fetchall_query(query, db_file)
    if output:
        print("\nАктивные записи:\n")
        print(tabulate(output))
        print()

    query = f'SELECT * from dhcp WHERE {key}="{value}" AND active = 0'
    output = fetchall_query(query, db_file)
    if output:
        print("Неактивные записи:\n")
        print(tabulate(output))


def get_all_data(db_file):
    query = f'SELECT * from dhcp WHERE active = 1'
    output = fetchall_query(query, db_file)
    if output:
        print("\nАктивные записи:\n")
        print(tabulate(output))
        print()

    query = f'SELECT * from dhcp WHERE active = 0'
    output = fetchall_query(query, db_file)
    if output:
        print("Неактивные записи:\n")
        print(tabulate(output))


def fetchall_query(query, db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    output = ""
    try:
        cursor.execute(query)
        output = cursor.fetchall()
    except sqlite3.OperationalError as err:
        print(f'Данный параметр "{db_file}" не поддерживается!')
        
    connection.commit()
    connection.close()
    return output
