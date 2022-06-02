# -*- coding: utf-8 -*-

"""
Задание 23.1

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать
исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра:
ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

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
    print(ip1.ip)
    print(ip1.mask)