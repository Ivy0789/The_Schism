"""
This file defines game combat
"""
import cmd
import math
import time

from colorama import Fore, Back, Style
from char import Hero
from char import generate
from core import call_ascii
from core import call_audio
from core import clear
from core import type_print
from pygame import mixer as mix
from random import choice
from random import choices
from random import randint


class Combat(cmd.Cmd):
    enemy_list = ['Goblin', 'Imp']
    last = 0
    player = Hero(name="",
                  health=100,
                  maxhp=100,
                  attack=10,
                  defense=10,
                  level=1,
                  exp=0,
                  )

    prompt = f'\n\t\t{Fore.RED}       You are in Combat!\n' \
             f'\n\t\t{Fore.GREEN}|  Attack  |  Item  |  Run  |{Fore.YELLOW}\n\n\t\t'

    def __init__(self, bag, loc=None, boss=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enemy = generate(self.player, boss)
        self.loc = loc
        self._bag = bag
        clear()
        print(Fore.RED), call_ascii(self.enemy.name), print(Fore.YELLOW)
        call_audio('battle')
        time.sleep(1.5)
        self.txt = {
            'intro': [
                f"A frenzied {self.enemy.name} appeared!",
                f"A terrifying {self.enemy.name} approaches!",
                f"{self.player.name} found a ferocious {self.enemy.name}!",
                f"Gah! An infelicitous {self.enemy.name} rushes toward {self.player.name}!",
                f"Oh no! A {self.enemy.name} rushes towards you!"
            ],
            'player': [
                f"{self.player.name} attacks!",
                f"{self.player.name} charges the enemy!",
                f"{self.player.name} lunges forward!",
                f"{self.player.name} rushes forward!"
            ],
            'enemy': [
                f"The {self.enemy.name} attacks!",
                f"The {self.enemy.name} charges forward, enraged!",
                f"The {self.enemy.name} lashes out!",
                f"The {self.enemy.name} angrily attacks!"
            ],
            'win': [
                f"{self.player.name} defeated the {self.enemy.name}!",
                f"{self.player.name} is victorious! The {self.enemy.name} is dead!",
                f"{self.player.name} did it! {self.player.name} Won!",
                f"{self.player.name} revels in victory over the {self.enemy.name}!"
            ],
            'run': [
                f"{self.player.name} tries to escape!",
                f"{self.player.name} searches for an exit!",
                f"Driven by fear, {self.player.name} prepares to run!",
                f"{self.player.name} tries to run away!"
            ],
            'fail': [
                f"Fail!",
                f"Unsuccessful!",
                f"{self.player.name} fell over instead!",
                f"{self.player.name} completely fudged it!",
                f"So much NO just happened!"
            ],
            'success': [
                f"Yes!",
                f"Success!",
                f"{self.player.name} did it!",
                f"Excellent!",
                f"Fabulous!",
                f"{Back.WHITE, Fore.BLACK}So Totally Excellent!{Style.RESET_ALL}{Fore.YELLOW}"
            ],
            'item': [
                f"{self.player.name} uses PLACEHOLDER"
            ],
            'hit': [
                f"A hit! A fine hit!",
                f"A strike!",
                f"A solid blow!",
                f"Epic strike!"
            ],
            'miss': [
                f"Gah! A miss!",
                f"The vicious attack hit only air!",
                f"Miss!",
                f"No good!"
            ]
        }

    def preloop(self) -> None:
        """
        This is a hook method of Cmd that executes only once as the cmdloop is called. This enables the initial combat
        message to print.
        """
        type_print(f"\n\t\tA magical portal opened and pulled you through!\n")
        type_print(f"\n\t\t{Fore.YELLOW}{choice(self.txt['intro'])}\n")
        print(self.player)
        print(self.enemy)

    def default(self, line: str) -> bool:
        """
        This is a Cmd method that determines what message prints if the prompt entered does not match a command
        """
        clear()
        print("Not a valid move!")
        return False

    def precmd(self, line: str) -> str:
        print(Fore.YELLOW)
        return line

    def postcmd(self, stop: bool, line: str) -> bool:
        """ Handles life check, exp, and exit conditions each loop """
        if not self.enemy.alive():  # checks if enemy is alive and generates exp gain
            mix.fadeout(1000)
            call_audio('win', 0)
            type_print(f"\t{choice(self.txt['win'])}")
            exp = self.gen_exp()
            self.player.exp += exp
            self.loot()
            type_print(f'\t\tYou gained {exp} points for defeating the {self.enemy.name}!'
                       f'\n\n\t\t You are level: {self.player.level}'
                       f'\n\n\t\tPress Enter to Return to {self.loc.name}....')
            call_audio('interlude')
            input("\n\n\t")
            clear()
            self.leave_combat()
        elif not self.player.alive():
            print("You are dead!")
            return True  # this terminates the program. todo link to lose sequence that asks 'play again?'
        else:
            clear()
            print(self.player)
            print(self.enemy)

    def leave_combat(self):
        """ This exits the combat module and returns the cmdloop to the Engine """
        del self.enemy
        mix.fadeout(1000)
        call_audio('dungeon')
        from game import Engine
        return Engine(bag=self._bag, room=self.loc.id).cmdloop() and False

    def player_first(self, power):  # attack
        """
        This method exists to reduce repetitious code. It simply places the player first in the move order.
        Args:
            power: the power of the used move
        """
        type_print(f"\t{choice(self.txt['player'])}")
        self.damage(self.player, self.enemy, power)
        time.sleep(.8)
        if self.enemy.alive():
            type_print(f"\t{choice(self.txt['enemy'])}")
            self.damage(self.enemy, self.player, 100)
        time.sleep(1.2)

    def enemy_first(self, power):  # attack
        """
        This method exists to reduce repetitious code. It simply places the enemy first in the move order.
        Args:
            power: power of move being used
        """
        type_print(f"\n\t{choice(self.txt['enemy'])}\n")
        self.damage(self.enemy, self.player, 100)
        time.sleep(.8)
        if self.player.alive():
            type_print(f"\n\t{choice(self.txt['player'])}")
            self.damage(self.player, self.enemy, power)
        time.sleep(1.2)

    def damage(self, user, target, power=100):  # attack
        """
            calculates damage dealt by characters to each other in combat. uses modified damage formula from the GOAT
            game series Pokémon. The formula can be found @ https://bulbapedia.bulbagarden.net/wiki/Damage
            it also adds a random hit element, with a 10% miss chance.
        Args:
            user: the character dealing damage. This will be a class instance
            target: the character taking damage. This will be a class instance
            power: the power level of the move being used, then outputs the appropriate randomized hit or miss
            message and how much damage was done to whom by whom.
        """
        dmg = (round(
            (((((2 * user.level) / 5) + 2) * (power * (user.attack / target.defense)) / 50) + 2)
            * (randint(100, 200) / 100)
            * (randint(100, 120) / 100))) + 2
        if self.rand_check() > 8:
            target.health -= dmg
        else:
            dmg = 0
        type_print('\t....\n\t....')
        time.sleep(1)
        type_print(f"\t{choice(self.txt['miss'])}" if dmg <= 0 else f"\t{choice(self.txt['hit'])}")
        type_print(f'\t'
                   f'{user.name} dealt '
                   f'{Fore.RED}{dmg if dmg > 0 else "no"} damage{Fore.YELLOW} to '
                   f'{target.name}!'
                   )

    def gen_exp(self):
        return round(((randint(350, 600) / math.log2(self.player.level if self.player.level > 1 else 2)) + 100)
                     if self.enemy.name in self.enemy_list else
                     ((randint(550, 800) / math.log2(self.player.level if self.player.level > 1 else 2)) + 100))

    def loot(self):
        loot_table = ['Potion', 'Apple', 'Salted Pork', 'Royal Pauldrons',
                      'Tome of Power', 'Mithril Chainmail', 'Light of Elune', 'Goblin Helm']
        r = randint(1, 100)
        if r > 50:
            loot = choices(loot_table, weights=[30, 30, 30, 1, 5, 1, 1, 0], k=2) if self.enemy.name != 'Goblin' \
                else choices(loot_table, weights=[30, 30, 30, 1, 5, 0, 1, 30], k=2)
            if loot:
                type_print(f"\t\t{self.enemy.name} dropped {', '.join(loot)}!")
                self._bag.check(loot)

    def rand_check(self):
        hit = randint(1, 100)
        while hit in range(self.last - 8, self.last + 8):
            hit = randint(1, 100)
        self.last = hit
        return hit

    # Action Commands
    def do_help(self, arg: str):
        """ Overrides default help menu """
        print(
            f"\n\tCombat Commands:\n"
            f"""\t\t{'attack'.ljust(8)} - Attack your foe! Quick moves first for less damage, "
                                                           Normal is 50/50 for normal damage, "
                                                           Power moves second for extra damage\n"""
            f"\t\t{'item'.ljust(8)} - Use an item! Beware, your enemy will not tarry...\n"
            f"\t\t{'run'.ljust(8)} - Try to run away! It might fail, and your enemy will surely strike!\n"
        )

    def do_attack(self, *_):
        """ Attack your enemy using one of three options """
        moves = ['quick', 'normal', 'power']
        atk = ''
        clear()
        print(f'\n\t\tWhat attack?\n\n\t\t{Fore.GREEN}|  Quick  |  Normal  |  Power  |\n\n{Fore.YELLOW}')
        while atk.lower() not in moves:
            atk = input("\t\t")
            atk.lower()
            if atk == 'quick':
                self.player_first(60)
                break
            if atk == 'normal':
                first = randint(1, 2)
                if first != 1:
                    self.player_first(100)
                    break
                if first != 2:
                    self.enemy_first(100)
                    break
            if atk == 'power':
                self.enemy_first(140)
                break
            if not 'quick' or 'normal' or 'power':
                type_print('\t\tThat is not a move!\n\n\t\t')

    def do_run(self, *_):
        """ Try to run away! """
        clear()
        type_print(f"\t{choice(self.txt['run'])}")
        type_print('\t....\n\t....'), time.sleep(1)
        if randint(0, 100) > 30:
            type_print(f"\t{choice(self.txt['success'])}")
            type_print(f'{self.player.name} ran away!')
            time.sleep(3)
            self.leave_combat()
        else:
            type_print(f"\t{choice(self.txt['fail'])}")
            self.damage(self.enemy, self.player, 100)

    def do_item(self, *_):
        """ Use an item! """
        self.player.use(self._bag.show_usable())
        self.damage(self.enemy, self.player, 100)
