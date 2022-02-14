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

in_path = str(argv[1])
add_path = ""

#add_path = "07_files/"   --- не работает без этого
#in_path = "config_sw1.txt"

with open(add_path + in_path) as f:
    for row in f:
        if row.replace(" ", "")[0] == "" or row.replace(" ", "")[0] == "!":
            pass
        else:
            if ((ignore[0] not in row) 
                    and ignore[1] not in row
                    and ignore[2] not in row):
                print(row.replace("\n", ""))
