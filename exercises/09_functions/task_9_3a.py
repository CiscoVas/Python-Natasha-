# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
                
            if "switchport mode access" in line:
                access_d[intf] = 1
            elif "switchport access vlan" in line:
                access_d[intf] = int(line.split()[-1])
            elif "switchport trunk allowed vlan" in line:
                trunk_d[intf] = [int(item) for item in line.split()[-1].split(",")]

    return access_d, trunk_d

add_path = "/"
#add_path = "/09_functions/"
path = os.getcwd() + add_path

#print(get_int_vlan_map("config_sw2.txt"))