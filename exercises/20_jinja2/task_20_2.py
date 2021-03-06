# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать шаблон templates/cisco_router_base.txt.

В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.

Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 20.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

"""

import task_20_1 as config_gen
import yaml


if __name__ == '__main__':
    with open('templates/cisco_router_base.txt', 'w') as wf:
        wf.write("{% include 'cisco_base.txt' %}\n\n")
        wf.write("{% include 'alias.txt' %}\n\n")
        wf.write("{% include 'eem_int_desc.txt' %}")

    with open('data_files/router_info.yml') as f:
        dict = yaml.safe_load(f)

    print(config_gen.generate_config('templates/cisco_router_base.txt', dict))
    