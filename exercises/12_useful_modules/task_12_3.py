# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""

from tabulate import tabulate


def print_ip_table(reachable_list, unreachable_list):
    something = {"Reachable": reachable_list, "Unreachable": unreachable_list}
    print(tabulate(something, headers="keys"))
    return 


if __name__ == "__main__":
    pos_list = ["1.1.1.1", "2.2.2.2", "5.5.5.5"]
    neg_list = ["3.3.3.3", "4.4.4.4"]
    print_ip_table(pos_list, neg_list)