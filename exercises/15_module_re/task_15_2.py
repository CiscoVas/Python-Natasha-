# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""
import os
import re

def parse_sh_ip_int_br(file_name):
    ''''
    Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
    * Interface
    * IP-Address
    * Status
    * Protocol

    Информация должна возвращаться в виде списка кортежей:
    [('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
    ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
    ('FastEthernet0/2', 'unassigned', 'down', 'down')]
    '''
    result = []
    with open (file_name) as f:
        reg_ip = r'(\S+\d+\S*) +(\S+) +\S+ +\S+ +(administratively +\S+|\S+)+ +(\S+)'
        
        for line in f:
            print(line)
            match = re.search(reg_ip, line)
            if match:
                result.append(match.groups())

    return result


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    print(parse_sh_ip_int_br(path + "sh_ip_int_br.txt"))
