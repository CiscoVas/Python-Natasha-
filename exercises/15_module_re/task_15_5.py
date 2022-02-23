# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""
import os
import re

def generate_description_from_cdp(config_file):
    '''
    Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
    на основании вывода команды описание для интерфейсов.

    Например, если у R1 такой вывод команды:
    R1>show cdp neighbors
    Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                    S - Switch, H - Host, I - IGMP, r - Repeater

    Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
    SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

    Для интерфейса Eth 0/0 надо сгенерировать такое описание
    description Connected to SW1 port Eth 0/1

    Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
    а значения - команда задающая описание интерфейса:
    'Eth 0/0': 'description Connected to SW1 port Eth 0/1'
    '''
    result = {}
    regex = r'\n(?P<r_device>\S+) +(?P<l_intf>\S+ +\S+) +\d+ +(?:R |T |B |S |H |I |r |P ){1,8} +\S+ +(?P<r_intf>\S+ +\S+)'

    with open(config_file) as conf_file:
        file_txt = conf_file.read()
        for m in re.finditer(regex, file_txt):
            result[m.group("l_intf")] = f'description Connected to {m.group("r_device")} port {m.group("r_intf")}'

    return result


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    print(generate_description_from_cdp(path + "sh_cdp_n_sw1.txt"))

