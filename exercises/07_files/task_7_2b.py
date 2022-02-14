# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

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
