# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску,
как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24, вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000


Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)


Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит
адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28 в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего
в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

long_addr = input("Input IP-address in format ip_addr/mask: ")
#long_addr = "10.1.1.1/24"

ip_addr = long_addr.split("/")[0]
netmask = int(long_addr.split("/")[1])

ip_addr.split(".")
oct1 = int(ip_addr.split(".")[0])
oct2 = int(ip_addr.split(".")[1])
oct3 = int(ip_addr.split(".")[2])
oct4 = int(ip_addr.split(".")[3])

bin_ip = ("{:08b}{:08b}{:08b}{:08b}").format(oct1, oct2, oct3, oct4)
net_ip = bin_ip[:netmask] + bin_ip[netmask:].replace("1", "0")

b_oct1 = int(net_ip[0:8], 2)
b_oct2 = int(net_ip[8:16], 2)
b_oct3 = int(net_ip[16:24], 2)
b_oct4 = int(net_ip[24:32], 2)


ip_output = (
  "\n" + "Network:" 
  + "\n" + "{:<8}  "   * 4 
  + "\n" + "{:>08b}  " * 4
  )
print(ip_output.format(b_oct1, b_oct2, b_oct3, b_oct4, b_oct1, b_oct2, b_oct3, b_oct4))

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