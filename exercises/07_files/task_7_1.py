# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

import os

#path = os.getcwd() + "/07_files/"  --- для работы, снизу, чтобы скрипт проверки пройти
path = os.getcwd() + "/"
f = open ((path + "ospf.txt"), "r")

for row in f.readlines():
    l = row.split()
    output = ("\nPrefix                {}\nAD/Metric             {}\nNext-Hop              {}\nLast update           {}\nOutbound Interface    {}")
    print(output.format(l[1], l[2].replace("[", "").replace("]", ""), l[4].replace(",", ""), l[5].replace(",", ""), l[6]))
