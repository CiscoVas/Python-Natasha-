# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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


    def send_config_commands(self, commands):
        result = ""
        self.telnet.write(self.to_bytes("conf t"))
        result += self.telnet.read_until(b"(config)#", timeout=3).decode("utf-8")
        
        if type(commands) == str:
            self.telnet.write(self.to_bytes(commands))
            result += self.telnet.read_until(b"(config)#", timeout=3).decode("utf-8")
        else:
            for command in commands:
                self.telnet.write(self.to_bytes(command))
                result += self.telnet.read_until(b"(config)#", timeout=3).decode("utf-8")
        self.telnet.write(self.to_bytes("end"))

        return result


if __name__ == "main":
    r1 = CiscoTelnet("192.168.100.1", "cisco", "cisco", "cisco")
    print(r1.send_config_commands('logging 10.1.1.1'))
    print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
