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

in_path = str(argv[1])
out_path = str(argv[2])

add_path = ""
#add_path = "07_files/"

#in_path = "config_sw1.txt"
#out_path = "config_sw1_out.txt"

with open(add_path + in_path) as src, open(add_path + out_path, 'w') as dest:
    for row in src:
        if row.replace(" ", "") == "" or row.replace(" ", "")[0] == "!":
            pass
        else:
            if ((ignore[0] not in row) 
                    and ignore[1] not in row
                    and ignore[2] not in row):
                dest.write(row)



'''
#in_path = argv[1]
#out_path = str(argv[2])
in_path = "config_sw1.txt"
out_path = "config_sw1_out.txt"
#path = os.getcwd() + "/07_files/"  --- для работы, снизу, чтобы скрипт проверки пройти
path = os.getcwd() + "/"

f_input = open((path + in_path), "r")
f_input = f_input.read().rstrip().split('\n')

print((path + out_path))
f_output = open((path + out_path), "w")

for row in f_input:
    if row.replace(" ", "") == "" or row.replace(" ", "")[0] == "!":
        pass
    else:
        if ((ignore[0] not in row) 
                and ignore[1] not in row
                and ignore[2] not in row):
            f_output.write("\n" + row)
            
f_output.close()
'''