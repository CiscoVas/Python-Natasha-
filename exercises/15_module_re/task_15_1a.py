# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
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
        r_intf = re.compile(r'^[i|I]nterface (\S+)')
        r_ip   = re.compile(r'ip address ((?:\d+\.){3}\d+) ((?:\d+\.){3}\d+)')

        intf = ""
        for line in f:
            m_intf = r_intf.search(line)
            if m_intf:
                intf = m_intf.group(1)
                continue
            m_ip = r_ip.search(line)
            if m_ip:
              result[intf] = m_ip.group(1, 2)

    return result


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    print(get_ip_from_cfg(path + "config_r1.txt"))
