# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import os

def get_int_vlan_map(config_filename):
    access_d = {}
    trunk_d = {}

    with (open(str(path) + str(config_filename), "r")) as f:
        for line in f:
            if "interface" in line and "Ethernet" in line:
                intf = line.split()[1]
                
            if "switchport access vlan" in line:
                access_d[intf] = int(line.split()[-1])
            elif "switchport trunk allowed vlan" in line:
                trunk_d[intf] = [int(item) for item in line.split()[-1].split(",")]

    return access_d, trunk_d

add_path = "/"
#add_path = "/09_functions/"
path = os.getcwd() + add_path

print(get_int_vlan_map("config_sw1.txt"))