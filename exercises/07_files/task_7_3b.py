# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

import os

#path = os.getcwd() + "/07_files/"  --- для работы, снизу, чтобы скрипт проверки пройти
path = os.getcwd() + "/"

f = open (path + "CAM_table.txt", "r")
f = f.read().rstrip().split('\n')
sorted_list = []

vlan_num = input("Enter VLAN number: ")
output = "{:6}  {:16}  {:10}"

for row in f:
    if len(row.replace(" ", "")) > 0 and row.replace(" ", "")[0].isdigit():
        if row.split()[0] == vlan_num:            
            print(output.format(row.split()[0], row.split()[1], row.split()[3]))
