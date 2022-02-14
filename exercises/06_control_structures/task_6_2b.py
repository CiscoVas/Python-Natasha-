# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from curses.ascii import isdigit

is_valid_ip = False

while not is_valid_ip:
    ip_addr = input("Input IP-address like '10.1.1.1': ")

    ch_seq = ""
    prev_char = "."
    dot_count = 0
    dig_count = 1

    if ip_addr[-1] == ".":
        print("Неправильный IP-адрес")
    else:
        for item in ip_addr:
            if item == "." and dot_count < 3 and prev_char != ".":
                dot_count += 1
                dig_count += 1
                ch_seq = ""
                continue
            try:
                ch_seq += item
                if int(ch_seq) > (-1) and int(ch_seq) < 256:
                    prev_char = item
                    pass
                else:
                    print("Неправильный IP-адрес")
                    break
            except:
                print("Неправильный IP-адрес")
                break
        else:
            if dig_count == 4:
                oct1 = int(ip_addr.split(".")[0])
                if ip_addr == "255.255.255.255":
                    print("local broadcast")
                    is_valid_ip = True
                elif ip_addr == "0.0.0.0":
                    print("unassigned")
                    is_valid_ip = True
                elif oct1 > 0 and oct1 < 224:
                    print("unicast")
                    is_valid_ip = True
                elif oct1 > 223 and oct1 < 240:
                    print("multicast")
                    is_valid_ip = True
                else:
                    print("unused")
                    is_valid_ip = True
            else:
                print("Неправильный IP-адрес")
