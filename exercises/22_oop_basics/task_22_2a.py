# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
import telnetlib
from textfsm import clitable


class CiscoTelnet:
    def to_bytes(self, line):
        return f"{line}\n".encode("utf-8")
    

    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self.telnet.write(self.to_bytes(username))
        
        self.telnet.read_until(b'Password')
        self.telnet.write(self.to_bytes(password))
        
        regex_idx, match, output = self.telnet.expect([b">", b"#"])
        if regex_idx == 0 and match.group() == b'>':
            self.telnet.write(self.to_bytes("enable"))
            self.telnet.read_until(b"Password")
            self.telnet.write(self.to_bytes(secret))
            self.telnet.read_until(b"#", timeout=5)


    def _write_line(self, input_str):
        self.telnet.write(self.to_bytes(input_str))


    def parse_to_list_dict(self, output, command, index_file="index", templ_path="templates"):
        cli_table = clitable.CliTable(index_file, templ_path)
        d_attr = {'Command': command, 'Vendor': 'cisco_ios'}
        cli_table.ParseCmd(output, d_attr)
        header = cli_table.header

        return [dict(zip(header, line)) for line in cli_table]


    def send_show_command(self, show, parse = True, templates = "templates", index = "index"):
        self.telnet.write(self.to_bytes(show))
        output = self.telnet.read_until(b"#", timeout=3).decode("utf-8")

        if parse == True:
            return self.parse_to_list_dict(output, show, index, templates)

        return output

if __name__ == "main":
    r1 = CiscoTelnet("192.168.100.1", "cisco", "cisco", "cisco")
    print(r1.send_show_command("sh ip int br"))
