# -*- coding: utf-8 -*-
'''
Задание 25.1

Для заданий 25 раздела нет тестов!

Необходимо создать два скрипта:

1. create_db.py
2. add_data.py


2 скрипт add_data.py - с помощью этого скрипта, выполняется добавление данных в БД.
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding
и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно
   также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу
(порядок добавления данных может быть произвольным, но сообщения должны
выводиться аналогично выводу ниже):

$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac


На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

'''
import os
import re
import yaml
import sqlite3
from tabulate import tabulate


def get_dhcp_list_from_text(output, device_name):
    regex = re.compile(
        r"\n(?P<mac>\w\w(?::\w\w){5}) +(?P<ip>\d+.\d+.\d+.\d+) +\d+ "
        r"+dhcp-snooping +(?P<vlan>\d+) +(?P<intf>\S+)"
    )
    # result_list = []
    # for match in regex.finditer(output):
    #     mac, ip, vlan, intf = match.group("mac", "ip", "vlan", "intf")
    #     result_list.append(match.groups() + (device_name, ))
    # return result_list
    return [match.groups() + (device_name, ) for match in regex.finditer(output)]


def fill_swithces_table(switches_yaml_path):
    with open(switches_yaml_path) as f:
        switches_d = yaml.safe_load(f)['switches']
        
    query = "INSERT into switches values (?, ?)"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    print("Добавляю данные в таблицу switches...")
    for row in switches_d.items():
        try:
            cursor.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных: {row} Возникла ошибка: {err}")
        
    connection.commit()
    connection.close()


def set_all_dhcp_to_false_activity():
    query = "UPDATE dhcp set active=0"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except sqlite3.IntegrityError as err:
        print(f"При обнуление статуса ACTIVE возникла ошибка: {err}")
        
    connection.commit()
    connection.close()


def first_fill_dhcp_table(file_path):
    output = ""
    full_list = []
    for file in file_path:
        device_name = file[:file.find("_dhcp"):]
        output = get_text_from_file(file)
        full_list.extend(get_dhcp_list_from_text(output, device_name))
    
    query = "INSERT into dhcp values (?, ?, ?, ?, ?, 1, datetime('now', '-31 day'))"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    for row in full_list:
        try:
            cursor.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных: {row} Возникла ошибка: {err}")
        
    connection.commit()
    connection.close()
    

def fill_dhcp_table(file_path):
    output = ""
    full_list = []

    for file in file_path:
        split_pathes = file.split("/")
        if len(split_pathes) > 1:
            file_name = split_pathes[-1::][0]
        else:
            file_name = file

        device_name = file_name[:file_name.find("_dhcp"):]
        output = get_text_from_file(file)
        full_list.extend(get_dhcp_list_from_text(output, device_name))
    
    # print(tabulate(full_list))
    set_all_dhcp_to_false_activity()

    query = "REPLACE into dhcp values (?, ?, ?, ?, ?, 1, datetime('now'))"
    conn = sqlite3.connect(db_name)
    for row in full_list:
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


def delete_old_macs_from_dhcp(expire_days):
    query = f"DELETE from dhcp WHERE last_active < datetime('now', '-{expire_days} day')"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


db_name = "dhcp_snooping.db"

if os.path.isfile(db_name):
    print("База данных существует!")
    fill_swithces_table("switches.yml")
    first_fill_dhcp_table(["sw1_dhcp_snooping.txt", "sw2_dhcp_snooping.txt", "sw3_dhcp_snooping.txt"])
    fill_dhcp_table(["new_data/sw1_dhcp_snooping.txt", "new_data/sw2_dhcp_snooping.txt", "new_data/sw3_dhcp_snooping.txt"])
    expire_days = 7
    delete_old_macs_from_dhcp(expire_days)
else:
    print("База данных не существует. Перед добавлением данных, ее надо создать")


if __name__ == "__main__":
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # cursor.execute('select * from switches')
    # print('select * from switches:')
    # print(cursor.fetchall())
    # print("*" * 75)

    cursor.execute('select * from dhcp')
    print('select * from dhcp:')
    print(tabulate(cursor.fetchall()))
    connection.close()
    pass
