# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import telnetlib
from textfsm import clitable


class CiscoTelnet:
    def to_bytes(self, line):
        return f"{line}\n".encode("utf-8")
    

    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.ip = ip
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


    def send_config_commands(self, commands, strict = True):
        result = ""
        
        if type(commands) == str:
            commands = [commands]
        commands = ["conf t", *commands, "end"]

        for command in commands:
            self.telnet.write(self.to_bytes(command))
            temp = self.telnet.read_until(b"#", timeout=3).decode("utf-8")
            
            if "% " in temp:
                temp_lines = temp.split("\n")
                err_lines = ""
                for line in temp_lines:
                    if "% " in line:
                        err_lines += f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {line}'
                    if strict == True: raise ValueError(temp)
                print(err_lines)
            result += temp

        return result


# r1 = CiscoTelnet("192.168.100.1", "cisco", "cisco", "cisco")
# commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
# correct_commands = ['logging buffered 20010', 'ip http server']
# commands = commands_with_errors+correct_commands
    
# print(r1.send_config_commands(commands_with_errors, strict=True))
# print(r1.send_config_commands(commands, strict=False))