# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from re import sub
import subprocess


def ping_ip_addresses(ip_list):
    pos_list = []
    neg_list = []

    for ip_addr in ip_list:
        result = subprocess.run(['ping', '-c', '2', '-n', ip_addr])
        if result.returncode == 0:
            pos_list.append(ip_addr)
        else:
            neg_list.append(ip_addr)
            
    return((pos_list, neg_list))

#print(ping_ip_addresses(["8.8.8.8"]))