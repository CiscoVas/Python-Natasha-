# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

"""

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

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        normalize_dict = {}
        for key, val in topology_dict.items():
            
            if not normalize_dict.get(val) == key:
                normalize_dict[key] = val
        
        return normalize_dict

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

if __name__ == "__main__":
    top = Topology(topology_example)
    top.delete_node("SW1")
    print(top.topology)
    top.delete_node("SW10")