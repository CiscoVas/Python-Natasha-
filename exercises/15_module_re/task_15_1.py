# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

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
    '''
    result = []
    with open (file_name) as f:
        reg_ip = r'ip address ((?:\d+\.){3}\d+) ((?:\d+\.){3}\d+)'

        for line in f:
            match_ip = re.search(reg_ip, line)
            if match_ip:
                result.append(match_ip.group(1, 2))

    return result


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    print(get_ip_from_cfg(path + "config_r1.txt"))
