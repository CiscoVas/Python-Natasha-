# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

import yaml
import task_20_5 as vpn_config_gen
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
            return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

def send_config_commands(device, config_commands):
    result = ""
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(config_commands)
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    return result

def get_tun_num(interfaces_r1, interfaces_r2):
    tun_nums_r1 = sorted([ int(intf_str.split(" ")[1].split("Tunnel")[1]) for intf_str in interfaces_r1.split("\n") if interfaces_r1])
    tun_nums_r2 = sorted([ int(intf_str.split(" ")[1].split("Tunnel")[1]) for intf_str in interfaces_r2.split("\n") if interfaces_r2])
    
    for i in range(0, 1024):
        if i in tun_nums_r1 or i in tun_nums_r2:
            pass
        else:
            return i

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    command = "sh run | inc ^interface Tunnel"

    interfaces_r1 = send_show_command(src_device_params, command)
    interfaces_r2 = send_show_command(dst_device_params, command)

    vpn_data_dict['tun_num'] = get_tun_num(interfaces_r1, interfaces_r2)

    r_src_commands, r_dst_commands = vpn_config_gen.create_vpn_config(src_template, dst_template, vpn_data_dict)
    dev_src_commands = send_config_commands(src_device_params, r_src_commands.split("\n"))
    dev_dst_commands = send_config_commands(dst_device_params, r_dst_commands.split("\n"))

    return dev_src_commands, dev_dst_commands


if __name__ == '__main__':
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    print(configure_vpn(devices[0], devices[1], 'templates/gre_ipsec_vpn_1.txt', 'templates/gre_ipsec_vpn_2.txt', data))
