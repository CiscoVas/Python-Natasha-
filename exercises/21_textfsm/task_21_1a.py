# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm

def parse_output_to_dict(template, command_output):
  with open(template) as f_temp:
    fsm = textfsm.TextFSM(f_temp)
    l_parse = fsm.ParseText(command_output)
    head = fsm.header
  # result = []
  
  # for line in l_parse:
  #   d = {key: val for key, val in zip(head, line)}
  #   result.append(d)
  # print(result)
  
  return [dict(zip(head, line)) for line in l_parse]

if __name__ == "__main__":
  with open("output/sh_ip_int_br.txt") as f:
    output = f.read()
  
  result = parse_output_to_dict("templates/sh_ip_int_br.template", output)