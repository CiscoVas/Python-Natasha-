# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import os
import re

from attr import asdict

def convert_ios_nat_to_asa(in_ios_nat_file, out_asa_nat_file):
    '''
    Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
    из синтаксиса cisco IOS в cisco ASA.

    Функция ожидает такие аргументы:
    - имя файла, в котором находится правила NAT Cisco IOS
    - имя файла, в который надо записать полученные правила NAT для ASA

    Функция ничего не возвращает.
    ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

    И соответствующие правила NAT для ASA:
    object network LOCAL_10.1.2.84
    host 10.1.2.84
    nat (inside,outside) static interface service tcp 22 20022
    '''
    asa_nat_temp = (
        "object network LOCAL_{ip}\n"
        " host {ip}\n"
        " nat (inside,outside) static interface service {transp} {p_in} {p_out}\n"
    )
    
    regex = r'ip nat inside source static (?P<transp>\w+) (?P<obj>\S+) (?P<p_in>\S+) interface \S+ (?P<p_out>\S+)'
    
    with open(in_ios_nat_file) as src, open(out_asa_nat_file, 'w') as dst:
        for line in src:
            match = re.search(regex, line)
            ip, transp, p_in, p_out = match.group('obj', 'transp', 'p_in', 'p_out')
            
            dst.write(asa_nat_temp.format(ip=ip, transp=transp, p_in=p_in, p_out=p_out))


if __name__ == "__main__":
    #add_path = "/"
    add_path = "/15_module_re/"
    path = os.getcwd() + add_path
    convert_ios_nat_to_asa(path + "cisco_nat_config.txt", path + "cisco_asa_nat.txt")

