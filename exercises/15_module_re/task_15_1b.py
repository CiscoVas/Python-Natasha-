# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них.

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import os
import re

def get_ip_from_cfg(file_name):
    ''''
    Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
    которые настроены на интерфейсах, в виде списка кортежей:
    * первый элемент кортежа - IP-адрес
    * второй элемент кортежа - маска
    {'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),

    interface Ethernet0/0
    description To PE_r3 Ethernet0/0
    bandwidth 100000
    ip address 10.0.13.1 255.255.255.0
    '''
    result = {}
    with open (file_name) as f:
        regex = re.compile(
            r'interface (?P<intf>\S+)\n'
            r'( .*\n)*'
            r' ip address +(?P<ip>\S+) +(?P<mask>\S+)\n'
            r'( ip address +(?P<sec_ip>\S+) +(?P<sec_mask>\S+) secondary)*'
        )

        match = regex.finditer(f.read())
        
        for m in match:
            if m.group("sec_ip"):
                result[m.group("intf")] = [m.group("ip", "mask"), m.group("sec_ip", "sec_mask")]
            else:
                result[m.group("intf")] = [m.group("ip", "mask")]

    return result


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    print(get_ip_from_cfg(path + "config_r2.txt"))
