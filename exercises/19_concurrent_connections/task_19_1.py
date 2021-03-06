# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
import yaml
from concurrent.futures import ThreadPoolExecutor


def ping_ip_address(ip_addr):
    ping_bool = subprocess.run(['ping', '-c', '2', '-n', ip_addr])
    return ping_bool.returncode == 0


def ping_ip_addresses(ip_list, limit = 3):
    pos_list = []
    neg_list = []

    with ThreadPoolExecutor(max_workers = limit) as executor:
        results = executor.map(ping_ip_address, ip_list)

    for device, res in zip(ip_list, results):
        if res:
            pos_list.append(device)
        else:
            neg_list.append(device)

    return pos_list, neg_list


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    ip_addrs = [dev.get("host") for dev in devices]
    print(ping_ip_addresses(ip_addrs, 3))
