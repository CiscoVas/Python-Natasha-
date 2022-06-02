# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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


    def __getitem__(self, index):
        items_list = [(key, val) for key, val in self.topology.items()]
        return items_list[index]


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
    top = Topology(topology_example)
    for link in top:
        print(link)