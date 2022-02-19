"""
This file defines game characters. It namely deals with the hero, but also random baddies.
"""
# Character list
import random
from colorama import Fore
from core import type_print
from random import randint


class Char(object):
    """
    Defines characters. This is the primary class, with Hero and Enemy classes inheriting its methods.
    The health, attack, defense, and leveling attributes are automatically updated using property decorators
    This allows both subclasses to utilize the same framework for combat purposes. Here is where character
    balance is achieved. See the readme for details on the attack formula and random enemy generator
    """

    def __init__(self, name: str, health: int, max_hp: int, attack: int, defense: int, level: int) -> None:
        self._name = name
        self._health = health
        self._max_hp = max_hp
        self._attack = attack
        self._defense = defense
        self._level = level

    def __str__(self):
        return (
            f"\n\n\t{Fore.YELLOW}{self.name}'s Status:\n\n\t|\tHealth: "
            f"{self.health_color(self.health)} / {self.cyan(self.max_hp)}"
            f"\t|\tAttack: {self.cyan(self.attack)}\t|\t Defense: {self.cyan(self.defense)}"
            f"\t|\tLevel: {self.cyan(self.level)}\t|\t\n"
                )

    @property
    def name(self) -> str:
        """ returns name """
        return Fore.LIGHTBLUE_EX + self._name + Fore.YELLOW

    @name.setter
    def name(self, username):
        """ sets name from outside class"""
        self._name = username

    @property
    def health(self) -> int:  # health start
        """ returns current health """
        return self._health

    @health.setter
    def health(self, delta):
        """ Sets health attribute and checks max """
        self._health = delta
        if self._health > self._max_hp:
            self._health = self._max_hp

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, delta):
        self._max_hp = delta

    @property
    def attack(self) -> int:  # attack start
        """ access to _attack protected value """
        return self._attack

    @attack.setter
    def attack(self, delta):
        """ sets attack """
        self._attack = delta
        if self._attack <= 0:
            self._attack = 1

    @property
    def defense(self) -> int:  # defense start
        """ access to _defense protected value """
        return self._defense

    @defense.setter
    def defense(self, delta):
        """ sets defense"""
        self._defense = delta
        if self._defense <= 0:
            self._defense = 1

    @property
    def level(self) -> int:  # level start
        """ access to _level protected value """
        return self._level

    @level.setter
    def level(self, delta):
        """ sets level to change """
        self._level = delta
        if self._level <= 0:
            self._level = 1

    def alive(self) -> bool:
        """ Checks if caller is alive """
        if self._health > 0:
            return True

    @staticmethod
    def green(txt):
        return f"{Fore.LIGHTGREEN_EX}{txt}{Fore.YELLOW}"

    @staticmethod
    def cyan(txt):
        return f"{Fore.LIGHTCYAN_EX}{txt}{Fore.YELLOW}"

    def health_color(self, txt):
        return f"{Fore.LIGHTRED_EX if self.health < self.max_hp else Fore.LIGHTCYAN_EX}{txt}{Fore.YELLOW}"

    def healing(self, item):
        """ determines the amount healed relative to player max-hp """
        if (self._health + item["health"]) <= self._max_hp:
            return item["health"]
        else:
            return self._max_hp - self._health

    def use(self, item=None):
        if item is not None:
            type_print(f"\t{self.name} used {self.green(item['name'])}!" if item['sort'] == 'usable'
                       else f"\t{self.name} equipped {self.green(item['name'])}!" if item['sort'] == 'equipable'
                       else '')
            if item['health'] > 0:
                print(f"\n\n\t\t{self.name} gained {self.cyan(self.healing(item))} health!")
                self.health += item['health']
            if item['attack'] > 0:
                self.attack += item['attack']
                print(f"\n\n\t\t{self.name} gained {self.cyan(item['attack'])} attack!")
            if item['defense'] > 0:
                self.defense += item['defense']
                print(f"\n\n\t\t{self.name} gained {self.cyan(item['defense'])} defense!")
            if item['power'] > 0:
                self.level += item['power']
                increase = round(10 * item['power'])
                type_print(f"\t{self.name} leveled up!")
                type_print(f"\t{self.name}'s max HP increased by {increase}!")
                self.max_hp += increase
                self.health += increase
            if item['health'] == 0 and item['attack'] == 0 and item['defense'] == 0 and item['power'] == 0:
                print(f"\n\n\t\t{self.green(item['name'])} did nothing! Why does it exist?! Why?!!")
            return True
        else:
            return 'exit'


class Hero(Char):
    """
    This defines the hero character and adds an exp field
    """

    def __init__(self, name, health, max_hp, attack, defense, level, exp, combat=True):
        super().__init__(name, health, max_hp, attack, defense, level)
        self._name = name
        self._exp = exp
        self._combat = combat

    @property
    def combat(self):
        return self._combat

    @property
    def name(self) -> str:
        return f"{Fore.LIGHTBLUE_EX}{self._name}{Fore.YELLOW}"

    @property
    def exp(self):
        """ fetches exp value """
        return self._exp

    @exp.setter
    def exp(self, delta):
        self._exp = delta
        if self._exp >= 1500:
            self._exp -= 1500
            self.level_up()

    def level_up(self):
        increase = 10
        type_print(f"\t{self.name} leveled up!")
        type_print(f"\t{self.name}'s max HP increased by {self.cyan(increase)}!")
        self.max_hp += increase
        self.level += 1


class Enemy(Char):
    """ Defines Enemy properties and generates random baddies """

    def __init__(self, name: str, health: int, max_hp: int, attack: int, defense: int, level: int):
        super().__init__(name, health, max_hp, attack, defense, level)
        self._name = name
        self._health = health
        self._max_hp = max_hp
        self._attack = attack
        self._defense = defense
        self.level = level

    @property
    def name(self) -> str:
        return Fore.LIGHTMAGENTA_EX + self._name + Fore.YELLOW

    def __str__(self):
        return f'\n\t\tThe {self.name} has {Fore.LIGHTRED_EX}{self.health}{Fore.YELLOW} health remaining!'


def generate(player, boss=False):
    """ Generates random enemies that have some semblance of scaling to player stats """
    enemy_list = ['Goblin', 'Troll', 'Imp', 'Warlock',
                  'Felhound', 'Saberclaw', 'Zombie']
    kind = random.choice(enemy_list)
    if boss:
        enemy = Enemy(
            name="Khakaron",
            health=player.max_hp,
            max_hp=player.max_hp,
            attack=player.attack + 2,
            defense=player.defense,
            level=player.level
                      )
        return enemy
    if not boss:
        mult = .6 if kind == 'Goblin' else \
            .7 if kind == 'Imp' else \
            .7 if kind == 'Zombie' else \
            1.1 if kind == 'Warlock' else 1

        enemy = Enemy(
            name=kind,
            health=round(100 * mult),
            max_hp=round(100 * mult),
            attack=abs(round(((player.attack - randint(7, 16)) * mult))),
            defense=abs(round(((player.defense - randint(7, 16)) * mult))),
            level=randint(player.level - 5, player.level)
                      )
        return enemy
