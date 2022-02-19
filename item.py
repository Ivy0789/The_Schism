"""
This file defines the item and inventory systems
"""
import json
from os import listdir
from os import path as p

import tabulate
from colorama import Fore
from core import clear


class Item(object):
    def __init__(self, name: str = str, health: int = int, attack: int = int, defense: int = int,
                 power: int = int, description: str = str, value: int = int, sort: str = str) -> None:
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.power = power
        self.description = description
        self.value = value
        self.sort = sort

    _index = []  # private index imported from file

    def get_item(self):
        """ Gets items from file and loads into index """
        for i in listdir(p.join("assets", "items")):
            with open(p.join("assets", "items", f'{i}')) as file:
                read = file.read()
                load = json.loads(read)
                load['name'] = ' '.join(
                    name.capitalize()
                    if name != 'of' else name
                    for name in i.replace('.json', '').split()
                )
                self._index.append(load)

    def __index__(self):
        item_index = [item for item in self._index]
        return item_index


class Bag(Item):
    def __init__(self, bag=None, counter=None):
        super().__init__()
        if bag is None:
            bag = [{
                "name": "Potion",
                "health": 20,
                "attack": 0,
                "defense": 0,
                "power": 0,
                "description": "Heal Thyself!",
                "value": 5,
                "sort": "usable"
            }]
        if counter is None:
            counter = ["Potion"]
        self._bag = bag
        self._counter = counter

    @property
    def bag(self):
        return self._bag

    def __index__(self):
        """ Returns: item, count, description """
        return [[item] for item in self._bag]\
            and [[item, self._counter.count(item)] for item in set(self._counter)]

    @property
    def counter(self) -> list:
        """ Sorts and counts usable items in bag for use func"""
        stripped = []
        for item in self._bag:
            if item['sort'] == 'usable' and item['name'] in self._counter:
                item.update({'count': self._counter.count(item['name'])})
                stripped.append([
                    '\t',
                    self.yellow(item["name"]),
                    self.yellow(item['count']),
                    self.blue(item['description'])
                                 ])
        return stripped

    def show_usable(self) -> dict or None:
        """ Shows only usable items when called """
        print(
            f'\n\t\tWhat would you like to use?\n'
            f'\n\t\tSimply type the item name!\n'
            f'\n\t\tType Exit to exit!\n\n'
        )
        header = ['Item Name', 'Quantity', 'Description\n\t']
        print('\t' + tabulate.tabulate(self.counter, headers=header, numalign='center',
                                       stralign='center', tablefmt='plain'))
        selection = ""
        while selection not in self._counter:
            selection = input(f'\n\t\t')
            selection = ' '.join(name.capitalize() if name != 'of' else name for name in selection.split())
            if selection == 'Exit':
                clear()
                return None
            if selection in self._counter:
                clear()
                for item in self._index:
                    if selection == item['name']:
                        selection = item
                        if selection['sort'] != 'equipable':
                            self._counter.remove(selection['name'])
                        return selection

    @staticmethod
    def blue(txt):
        """ Turns text blue """
        return f"{Fore.LIGHTBLUE_EX}{txt}{Fore.YELLOW}"

    @staticmethod
    def yellow(txt):
        """ Turns text yellow """
        return f"{Fore.LIGHTYELLOW_EX}{txt}{Fore.YELLOW}"

    def check(self, item: list) -> None:
        """
        manages bag items and maintains a counter list matched to item names.
        Args:
            item (list): list of items in room
        """
        for ind in self._index:
            for val in item:
                if ind['name'] == val:
                    val = ind  # sets val to values in total item index for each item.
                    if val['name'] in [have['name'] for have in self._bag]:
                        self._counter.append(val['name'])
                    if val['name'] not in [have['name'] for have in self._bag]:
                        self._counter.append((val['name']))
                        self._bag.append(val)
