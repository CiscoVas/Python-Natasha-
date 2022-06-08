# -*- coding: utf-8 -*-
'''
Задание 25.1

Для заданий 25 раздела нет тестов!

Необходимо создать два скрипта:

1. create_db.py
2. add_data.py


1 скрипт create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
* должна выполняться проверка наличия файла БД
* если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
  должна быть создана БД
* имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует


Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

'''
import os
import sqlite3
from tabulate import tabulate


def create_db(db_file_path, create_script_path):
    create_script_str = get_script_from_file(create_script_path)
    
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.executescript(create_script_str)


def get_script_from_file(file_path):
    with open(file_path) as f:
        script = f.read()
    return script

db_name = "dhcp_snooping.db"
path_to_create_script = "dhcp_snooping_schema.sql"

if os.path.isfile(db_name):
    print("База данных существует!")
else:
    print("Создаю базу данных...")
    create_db(db_name, path_to_create_script)


if __name__ == "__main__":
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # cursor.execute('select * from switches')
    # print('select * from switches:')
    # print(cursor.fetchall())
    # print("*" * 75)

    cursor.execute('select * from sqlite_schema')
    print('select * from dhcp:')
    print(tabulate(cursor.fetchall()))
    pass