# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import os
import re
import csv

def write_dhcp_snooping_to_csv(filenames, output):
    ''''
    обрабатывает вывод команды show dhcp snooping binding из разных файлов и записывает обработанные
    данные в csv файл.

    Аргументы функции:
    * filenames - список с именами файлов с выводом show dhcp snooping binding
    * output - имя файла в формате csv, в который будет записан результат

    Функция ничего не возвращает.

    Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
    MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
    ------------------  ---------------  ----------  -------------  ----  --------------------
    00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
    00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
    Total number of bindings: 2

    В итоговом csv файле должно быть такое содержимое:
    switch,mac,ip,vlan,interface
    sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
    sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

    Первый столбец в csv файле имя коммутатора надо получить из имени файла,
    остальные - из содержимого в файлах.

    Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
    sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
    '''
    add_path = "/"
    #add_path = "/17_serialization/"
    path = os.getcwd() + add_path
    
    with open(output, "w") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["switch", "mac", "ip", "vlan", "interface"])

        for f_name in filenames:
            regex = r'^([a-zA-Z0-9]+)_'
            first_col = re.search(regex, f_name).group(1)

            with open(path + f_name) as f_in:
                
                regex = re.compile(r'\n((?:\w\w:)+\w\w) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
                match = regex.finditer(f_in.read())

                for m in match:
                    row = list(m.groups())
                    row.insert(0, first_col)
                    writer.writerow(row)
    

if __name__ == "__main__":
    write_dhcp_snooping_to_csv(["sw1_dhcp_snooping.txt", "sw2_dhcp_snooping.txt", "sw3_dhcp_snooping.txt"], "output.csv")
