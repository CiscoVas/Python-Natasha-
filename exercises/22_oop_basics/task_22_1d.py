# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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
    top = Topology(topology_example)
    print(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))