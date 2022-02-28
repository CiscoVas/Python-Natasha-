# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import os
import yaml
import graphviz
from draw_network_graph import draw_topology


def unique_network_map(topology_dict):
    '''
    Will delete all "duplicated" items from topology_dict and return result dicrionary with unique items
    '''
    result_d = {}
    for key, val in topology_dict.items():
        if val == "": 
            continue

        for second_key, second_val in topology_dict.items():
            if key == second_val and val == second_key:
                topology_dict[second_key] = ""
                #print('"Duplicate" item detected!')
        
        result_d[key] = val
        
    return result_d


def transform_topology(yaml_f_name):
    with open(yaml_f_name) as f_in:
        d = yaml.safe_load(f_in)
        norm_dict = {}

        for key in d.keys():
            for second_key in d[key].keys():
                for item in d[key][second_key].items():
                    norm_dict[(key, second_key)] = item 
        result_dict = unique_network_map(norm_dict)
    return result_dict


if __name__ == "__main__":
    add_path = "/"
    add_path = "/17_serialization/"
    path = os.getcwd() + add_path
    
    draw_topology(transform_topology(path + "topology.yaml"), out_filename = path + "test.png")
    #print(transform_topology(path + "topology.yaml"))