# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()

    def send_config_set(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        all_output = ""

        for command in commands:
            temp = super().send_config_set(command, exit_config_mode=False)
            self._check_error_in_command(command, temp)
            all_output += temp
        self.exit_config_mode()

        return all_output

    def send_command(self, command):
        output = super().send_command(command)
        self._check_error_in_command(command, output)
        return output

    def _check_error_in_command(self, command, command_output):
        if "% " in command_output:
            temp_lines = command_output.split("\n")
            for line in temp_lines:
                if "% " in line:
                    err_line = f'При выполнении команды "{command}" на устройстве {self.host} возникла ошибка -> {line}'
                    raise ErrorInCommand(err_line)
        return 

if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    r1.send_config_set('lo')