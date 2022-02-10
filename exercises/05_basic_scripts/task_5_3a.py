# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]

d_questions = {"access" : 'Введите номер VLAN:', "trunk" : 'Введите разрешенные VLANы:'}
switchport_mode = input("Input interface mode (access/trunk): ")
interface = input('Input interface name and ID like "Fa0/1": ')
vlans = input(d_questions.setdefault(switchport_mode))

#switchport_mode = "trunk"
#interface = "Fa0/7"
#vlans = "10, 20, 30"

template_dict = {"access" : access_template, "trunk" : trunk_template}

print("\n" + "interface " + interface)
print("\n".join(template_dict[switchport_mode]).format(vlans))