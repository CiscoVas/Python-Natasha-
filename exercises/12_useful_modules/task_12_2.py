# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

import ipaddress


def get_long_ip(ip1, oct4):
    oct1, oct2, oct3, _ = ip1.split(".")
    return ".".join([oct1, oct2, oct3, oct4])

def get_ip_list_from_two_ip(line):
    result = []
    item1, item2 = line.split("-")
    
    if not "." in item2:
        item2 = get_long_ip(item1, item2)

    while ipaddress.IPv4Address(item2) >= ipaddress.IPv4Address(item1):
        result.append(item1)
        item1 = str(ipaddress.IPv4Address(item1) + 1)

    return result

def convert_ranges_to_ip_list(ranges_list):
    result = []
    for item in ranges_list:
        if "-" in item:
            result.extend(get_ip_list_from_two_ip(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.40.128-172.21.41.132']))