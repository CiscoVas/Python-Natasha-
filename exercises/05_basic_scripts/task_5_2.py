# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
long_addr = input("Input IP-address in format ip_addr/mask: ")

ip_addr = long_addr.split("/")[0]
netmask = int(long_addr.split("/")[1])

ip_addr.split(".")
oct1 = int(ip_addr.split(".")[0])
oct2 = int(ip_addr.split(".")[1])
oct3 = int(ip_addr.split(".")[2])
oct4 = int(ip_addr.split(".")[3])

ip_output = (
  "\n" + "Network:" 
  + "\n" + "{:<8}  " * 4 
  + "\n" + "{:08b}  " * 4
  )
print(ip_output.format(oct1, oct2, oct3, oct4, oct1, oct2, oct3, oct4))

bit_mask = "1" * netmask + "0" * (32 - netmask)
m_oct1 = bit_mask[0:8]
m_oct2 = bit_mask[8:16]
m_oct3 = bit_mask[16:24]
m_oct4 = bit_mask[24:32]

net_output = (
  "\n" + "Mask:" 
  + "\n" + "/" + str(netmask)
  + "\n" + "{:<8}  " * 4 
  + "\n" + "{:<8}  " * 4 
  + "\n"
  )

print(net_output.format(int(m_oct1, 2), int(m_oct2, 2), int(m_oct3, 2), int(m_oct4, 2), 
                        m_oct1, m_oct2, m_oct3, m_oct4))
