# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from curses.ascii import isdigit
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
         elif ip_addr == "0.0.0.0":
            print("unassigned")
         elif oct1 > 0 and oct1 < 224:
            print("unicast")
         elif oct1 > 223 and oct1 < 240:
            print("multicast")
         else: print("unused")
      else:
         print("Неправильный IP-адрес")         
