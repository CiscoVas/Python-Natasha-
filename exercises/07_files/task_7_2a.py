# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv
import os

arg1 = argv[1]
#arg1 = "config_sw1.txt"
#path = os.getcwd() + "/07_files/"  --- для работы, снизу, чтобы скрипт проверки пройти
path = os.getcwd() + "/"

f = open ((path + arg1), "r")
f = f.read().rstrip().split('\n')

for row in f:
    if row.replace(" ", "") == "" or row.replace(" ", "")[0] == "!":
        pass
    else:
        if ((ignore[0] not in row) 
                and ignore[1] not in row
                and ignore[2] not in row):
            print(row)
