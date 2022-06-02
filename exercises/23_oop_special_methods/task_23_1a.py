# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress:
    def __init__(self, long_ip):
        ip, mask = long_ip.split("/")
        if not self._is_valid_ip(ip):
            raise ValueError("Incorrect IPv4 address")
        elif not self._is_valid_mask(mask):
            raise ValueError("Incorrect mask")
        else:
            self.ip = ip
            self.mask = int(mask)

    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"

    def _is_valid_ip(self, ip):
        while not False:
            ch_seq = ""
            prev_char = "."
            dot_count = 0
            dig_count = 1

            if (ip[-1] == ".") or (ip[0] == "."):
                return False
            else:
                for item in ip:
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
                            return False
                    except:
                        return False
                else:
                    if dig_count == 4:
                        return True
        
    def _is_valid_mask(self, mask):
        try:
            if int(mask) >= 8 and int(mask) <= 32:
                return True
            else:
                return False
        except:
            return False


if __name__ == "__main__":
    ip1 = IPAddress('10.1.1.254/24')
    print(ip1)

    ip_list = []
    ip_list.append(ip1)
    print(ip_list)
    # [IPAddress('10.1.1.1/24')]