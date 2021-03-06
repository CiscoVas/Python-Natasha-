# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент
вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое
файла в строку, а затем передать строку как аргумент функции (как передать вывод
команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция должна
работать и на других файлах (тест проверяет работу функции на выводе
из sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import os

def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
    main_dev = ""
    start_parse = False
    result_d = {}

    for cmd_line in command_output.split("\n"):
        if "show cdp neighbors" in cmd_line:
            if ">" in cmd_line:
                main_dev = cmd_line.split(">")[0]
            elif  "#" in cmd_line:
                main_dev = cmd_line.split("#")[0]
        
        if start_parse and cmd_line.strip() != "":
            remote_dev, local_intf_name, local_intf_id, *other, remote_intf_name, remote_intf_id = cmd_line.split()
            result_d[tuple([main_dev, local_intf_name + local_intf_id])] = tuple([remote_dev, remote_intf_name + remote_intf_id])

        if "Device ID" in cmd_line:
            start_parse = True
    
    return result_d


if __name__ == "__main__":
    add_path = "/"
    #add_path = "/11_modules/"
    path = os.getcwd() + add_path

    with open(path + "sh_cdp_n_sw1.txt") as f:
        print(parse_cdp_neighbors(f.read()))
