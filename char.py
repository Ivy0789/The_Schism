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

    def __init__(self, name: str, health: int, attack: int, defense: int, level: int) -> None:
        self._name = name
        self._health = health
        self._attack = attack
        self._defense = defense
        self._level = level

    def __str__(self):
        return (f"\n\n\t{Fore.YELLOW}{self._name}'s Status:\n\n\t|\tHealth: "
                f"{Fore.LIGHTRED_EX if self.health < 100 else Fore.GREEN}{self.health}{Fore.YELLOW} / 100"
                f"\t|\tAttack: {self.attack}\t|\t Defense: {self.defense}"
                f"\t|\tLevel: {self.level}\t|\t\n\n"
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
        """ Sets and limits value of health by the min of max hp, max of healing sources."""
        self._health = delta
        if self._health > 100:
            self._health = 100

    @property
    def attack(self) -> int:  # attack start
        """ access to _attack protected value """
        return self._attack

    @attack.setter
    def attack(self, delta):
        """ sets attack """
        self._attack = delta

    @property
    def defense(self) -> int:  # defense start
        """ access to _defense protected value """
        return self._defense

    @defense.setter
    def defense(self, delta):
        """ sets defense"""
        self._defense = delta

    @property
    def level(self) -> int:  # level start
        """ access to _level protected value """
        return self._level

    @level.setter
    def level(self, delta):
        """ sets level to change """
        self._level = delta

    def alive(self) -> bool:
        """ Checks if caller is alive """
        if self._health > 0:
            return True

    def use(self, item=None):
        if item is not None:
            type_print(f"\n\n\t{self.name} used {item['name']}!\n" if item['sort'] == 'usable'
                       else f"\n\t{self.name} equipped {item['name']}!\n")
            if item['health'] > 0:
                self.health += item['health']
                type_print(f"\n\t\t{self.name} gained {item['health']} health!\n")
            if item['attack'] > 0:
                self.attack += item['attack']
                type_print(f"\n\t\t{self.name} gained {item['attack']} attack!\n")
            if item['defense'] > 0:
                self.defense += item['defense']
                type_print(f"\n\t\t{self.name} gained {item['defense']} defense!\n")
            if item['power'] > 0:
                self.level += item['power']
                type_print(f"\n\t\t{self.name} gained {item['power']} level!\n")


class Hero(Char):
    """
    This defines the hero character and adds an exp field
    """

    def __init__(self, name, health, attack, defense, level, exp):
        super().__init__(name, health, attack, defense, level)
        self._name = name
        self._exp = exp

    @property
    def name(self) -> str:
        return Fore.LIGHTBLUE_EX + self._name + Fore.YELLOW

    @property
    def exp(self):
        """ fetches exp value """
        return self._exp

    @exp.setter
    def exp(self, delta):
        self._exp = delta


class Enemy(Char):
    """ Defines Enemy properties and generates random baddies """

    def __init__(self, name: str, health: int, attack: int, defense: int, level: int):
        super().__init__(name, health, attack, defense, level)
        self._name = name
        self._health = health
        self._attack = attack
        self._defense = defense
        self.level = level

    @property
    def name(self) -> str:
        return Fore.LIGHTMAGENTA_EX + self._name + Fore.YELLOW

    def __str__(self):
        return f'\n\t\tThe {self.name} has {Fore.LIGHTRED_EX}{self.health}{Fore.YELLOW} health remaining!'


def generate(player, boss=False):  # generates random enemies that hopefully scale based on player stats
    enemy_list = ['Goblin', 'Troll', 'Imp', 'Warlock',
                  'Felhound', 'Saberclaw', 'Zombie']
    kind = random.choice(enemy_list)
    if boss:
        enemy = Enemy(name="Drak'Tul",
                      health=130,
                      attack=player.attack - randint(5, randint(7, 10)),
                      defense=player.defense - randint(5, randint(7, 10)),
                      level=player.level + 1
                      )
        return enemy
    if not boss:
        mult = .8 if kind == 'Goblin' else \
            .7 if kind == 'Imp' else \
            .9 if kind == 'Zombie' else \
            1.2 if kind == 'Troll' else \
            1.3 if kind == 'Warlock' else 1

        enemy = Enemy(name=kind[0],
                      health=100 * mult,
                      attack=(player.attack - randint((player.attack - 5), player.attack - 1) * mult),
                      defense=(player.defense - randint((player.defense - 5), player.defense - 1) * mult),
                      level=player.level)
        return enemy
