# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
"""

import pprint


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

topology_example2 = {
    ("R1", "Eth0/4"): ("R7", "Eth0/0"),
    ("R1", "Eth0/6"): ("R9", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        normalize_dict = {}
        for key, val in topology_dict.items():
            
            if not normalize_dict.get(val) == key:
                normalize_dict[key] = val
        
        return normalize_dict


    def __add__(self, other_top):
        self_copy = Topology(self.topology.copy())

        for local_link, remote_link in other_top.topology.items():
            self_copy.add_link(local_link, remote_link)

        return self_copy

    def delete_link(self, key, val):
        if self.topology.get(key) and self.topology[key] == val:
            del self.topology[key]
        elif self.topology.get(val) and self.topology[val] == key:
            del self.topology[val]
        else:
            print("Такого соединения нет")

    def delete_node(self, node_name):
        keys_to_del = []
        for key, val in self.topology.items():
            local_node = key[0]
            remote_node = val[0]
            if local_node == node_name or remote_node == node_name:
                keys_to_del.append(key)
        if len(keys_to_del) == 0:
            print("Такого устройства нет")
        else:
            for key in keys_to_del:
                del self.topology[key]

    def add_link(self, local_link, remote_link):
        if self.topology.get(local_link):
            if self.topology[local_link] == remote_link:
                print("Такое соединение существует")
                return
            else:
                print("Cоединение с одним из портов существует")
                return
        elif self.topology.get(remote_link):
            print("Cоединение с одним из портов существует")
            return
        else:
            self.topology[local_link] = remote_link

if __name__ == "__main__":
    t1 = Topology(topology_example)
    t2 = Topology(topology_example2)
    t3 = t1 + t2

    print("T3___TOPOLOGY:")
    pprint.pprint(t3.topology)
    print("*" * 55)

    print("T2___TOPOLOGY:")
    pprint.pprint(t2.topology)
    print("*" * 55)

    print("T1___TOPOLOGY:")
    pprint.pprint(t1.topology)
    print("*" * 55)