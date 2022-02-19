"""
This file defines game combat
"""
import cmd
import math
import time

from colorama import Fore, Back, Style
from char import generate
from core import call_ascii
from core import call_audio
from core import call_music
from core import clear
from core import type_print
from pygame import mixer
from random import choice
from random import choices
from random import randint


class Combat(cmd.Cmd):
    enemy_list = ['Goblin', 'Imp']
    last = 0
    prompt = f'\n\t\t{Fore.RED}       You are in Combat!\n' \
             f'\n\t\t|{Fore.LIGHTGREEN_EX}  Attack  {Fore.YELLOW}' \
             f'|{Fore.LIGHTGREEN_EX}  Item  {Fore.YELLOW}' \
             f'|{Fore.LIGHTGREEN_EX}  Run  {Fore.YELLOW}|\n\n\t\t'

    def __init__(self, player, bag, loc=None, boss=False, equipped=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enemy = generate(player, boss)
        self.loc = loc
        self._bag = bag
        self._player = player
        self._equipped = equipped
        self._boss = boss
        clear()
        print(Fore.RED), call_ascii(self.enemy.name), print(Fore.YELLOW)
        time.sleep(1.6)
        self.txt = {
            'intro': [
                f"A frenzied {self.enemy.name} appeared!",
                f"A terrifying {self.enemy.name} approaches!",
                f"{self._player.name} found a ferocious {self.enemy.name}!",
                f"Gah! An infelicitous {self.enemy.name} rushes toward {self._player.name}!",
                f"Oh no! A {self.enemy.name} rushes towards you!"
            ],
            'player': [
                f"{self._player.name} attacks!",
                f"{self._player.name} charges the enemy!",
                f"{self._player.name} lunges forward!",
                f"{self._player.name} rushes forward!"
            ],
            'enemy': [
                f"The {self.enemy.name} attacks!",
                f"The {self.enemy.name} charges forward, enraged!",
                f"The {self.enemy.name} lashes out!",
                f"The {self.enemy.name} attacks angrily!"
            ],
            'boss': [
                f"{self.enemy.name} attacks!",
                f"{self.enemy.name} charges forward, enraged!",
                f"{self.enemy.name} lashes out!",
                f"{self.enemy.name} attacks angrily!"
            ],
            'win': [
                f"{self._player.name} defeated the {self.enemy.name}!",
                f"{self._player.name} is victorious! The {self.enemy.name} is dead!",
                f"{self._player.name} did it! {self._player.name} Won!",
                f"{self._player.name} revels in victory over the {self.enemy.name}!"
            ],
            'run': [
                f"{self._player.name} tries to escape!",
                f"{self._player.name} searches for an exit!",
                f"Driven by fear, {self._player.name} prepares to run!",
                f"{self._player.name} tries to run away!"
            ],
            'fail': [
                f"Fail!",
                f"Unsuccessful!",
                f"{self._player.name} fell over instead!",
                f"{self._player.name} completely fudged it!",
                f"So much NO just happened!"
            ],
            'success': [
                f"Yes!",
                f"Success!",
                f"{self._player.name} did it!",
                f"Excellent!",
                f"Fabulous!",
                f"{Back.WHITE, Fore.BLACK}So Totally Excellent!{Style.RESET_ALL}{Fore.YELLOW}"
            ],
            'item': [
                f"{self._player.name} uses PLACEHOLDER"
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
        type_print(f"\tA magical portal opened and pulled you through!")
        type_print(f"\t{Fore.YELLOW}{choice(self.txt['intro'])}") if not self._boss \
            else type_print(f"\t{self.enemy.name} rises from the shadows, eyes ablaze with fel fire!")
        print(self._player)
        print(self.enemy)

    def default(self, line: str) -> bool:
        """
        This is a Cmd method that determines what message prints if the prompt entered does not match a command
        """
        clear()
        print(self.red("\tNot a valid move!"))
        return False

    def precmd(self, line: str) -> str:
        """ This is a hook method of Cmd that executes immediately after input but before command dispatch. """
        print(Fore.YELLOW)
        if self._boss:
            immolate = randint(5, 15)
            self._player.health -= immolate
            type_print(f"\t{self._player.name} took {self.red(immolate)} damage from {self.enemy.name}'s Immolate!")
        return line

    def postcmd(self, stop: bool, line: str) -> bool:
        """ Handles life check, exp, and exit conditions each loop """
        if not self.enemy.alive():
            mixer.fadeout(1000)
            type_print(f"\t{choice(self.txt['win'])}")
            if not self._boss:
                call_audio('win', 0)
                exp = self.gen_exp()
                self._player.exp += exp
                self.loot()
                time.sleep(1.8)
                call_audio('interlude')
                type_print(
                    f'\t\tYou gained {exp} experience points for defeating the {self.enemy.name}!'
                    f'\n\n\t\tYou have {self._player.exp}/1500 experience points!'
                    f'\n\n\t\tYou are level: {self._player.level}'
                    f'\n\n\t\tPress Enter to Return to {self.loc.name}....'
                )
                input("\n\n\t")
                clear()
                self.leave_combat()
            else:
                del self.enemy
                from game import victory
                victory(self._player)
                return True
        elif not self._player.alive():
            type_print('\tYou have died!')
            from game import game_over
            game_over()
            return True
        else:
            print(self._player)
            print(self.enemy)
            return False

    def leave_combat(self):
        """ This exits the combat module and returns the cmdloop to the Engine """
        del self.enemy
        type_print("\tTraveling....")
        time.sleep(1)
        mixer.fadeout(1000)
        call_music()
        from game import Engine
        return Engine(player=self._player, bag=self._bag, room=self.loc.id, equipped=self._equipped).cmdloop() and False

    def player_first(self, power):  # attack
        """
        This method exists to reduce repetitious code. It simply places the player first in the move order.
        Args:
            power: the power of the used move
        """
        type_print(f"\t{choice(self.txt['player'])}")
        self.damage(self._player, self.enemy, power)
        time.sleep(.8)
        boss_name = "Khakaron"
        if self.enemy.alive():
            type_print(f"\t{choice((self.txt['enemy']) if self.enemy.name != boss_name else (self.txt['boss']))}")
            self.damage(self.enemy, self._player, 100)
        time.sleep(1.5)
        clear()

    def enemy_first(self, power):  # attack
        """
        This method exists to reduce repetitious code. It simply places the enemy first in the move order.
        Args:
            power: power of move being used
        """
        type_print(f"\t{choice(self.txt['enemy'])}")
        self.damage(self.enemy, self._player, 100)
        time.sleep(.8)
        if self._player.alive():
            type_print(f"\t{choice(self.txt['player'])}")
            self.damage(self._player, self.enemy, power)
        time.sleep(1.5)
        clear()

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
            * (randint(100, 120) / 100))) + 5
        hit = self.hit_check()
        if hit > 8:
            if user.name == self._player.name:
                dmg += sum([i['attack'] for i in self._equipped])
            else:
                dmg -= round((sum(i['defense'] for i in self._equipped)) * .15)
                dmg += self.enemy.attack if self.enemy.attack <= 10 else randint(6, 9)
        else:
            dmg = 0
        target.health -= dmg
        type_print('\t.........')
        time.sleep(.8)
        type_print(f"\t{choice(self.txt['miss'])}" if dmg <= 0 else f"\t{choice(self.txt['hit'])}")
        type_print(f'\t{user.name} dealt {self.red(dmg if dmg > 0 else "no")} damage to {target.name}!')

    def gen_exp(self):
        return round(((randint(350, 600) / math.log2(self._player.level if self._player.level > 1 else 2)) + 100)
                     if self.enemy.name in self.enemy_list else
                     ((randint(550, 800) / math.log2(self._player.level if self._player.level > 1 else 2)) + 100))

    def loot(self):
        """ generates loot from given table """
        loot_table = ['Potion', 'Apple', 'Salted Pork', 'Royal Pauldrons',
                      'Tome of Power', 'Mithril Chainmail', 'Light of Elune', 'Goblin Helm']
        r = randint(1, 100)
        if r > 33:
            loot = choices(loot_table, weights=[30, 50, 30, 3, 5, 1, 1, 0], k=2) if self.enemy.name != 'Goblin' \
                else choices(loot_table, weights=[30, 50, 30, 3, 5, 0, 1, 30], k=2)
            if loot:
                type_print(
                    f"\t{self.enemy.name} dropped: {Fore.LIGHTGREEN_EX}"
                    f"""{f'{Fore.YELLOW} and {Fore.LIGHTGREEN_EX}'.join(loot)
                    if len(loot) > 1 else ''.join(loot)
                    if len(loot) == 1 else 'nothing'
                    }!{Fore.YELLOW}"""
                )
                self._bag.check(loot)

    def hit_check(self):
        """ This ensures two misses should not occur in a row. """
        hit = randint(1, 100)
        if hit in range(self.last - 8, self.last + 8):
            hit = randint(10, 100)
        self.last = hit
        return hit

    @staticmethod
    def red(txt):
        """ Turn text red """
        return f"{Fore.RED}{txt}{Fore.YELLOW}"

    @staticmethod
    def yellow(txt):
        """ Turn text yellow """
        return f"{Fore.LIGHTYELLOW_EX}{txt}{Fore.YELLOW}"

    @staticmethod
    def green(txt):
        """ Turn text green """
        return f"{Fore.LIGHTGREEN_EX}{txt}{Fore.YELLOW}"

    # Action Methods
    def do_help(self, arg: str):
        """ Overrides default help menu """
        clear()
        print(
            f"""
            {self.yellow('Combat Commands:')}
            \t{'attack'.ljust(8)} - Attack your foe! 
            \t\t{(self.yellow('quick')).ljust(8)} - moves first for less damage
            \t\t{(self.yellow('normal')).ljust(8)} - is 50/50 for normal damage
            \t\t{(self.yellow('power')).ljust(8)} - moves second for extra damage
            \t{'item'.ljust(8)} - Use an item! Beware, your enemy will not tarry...
            \t{'run'.ljust(8)} - Try to run away! It might fail, and your enemy will surely strike!
            """
        )

    def do_attack(self, *_):
        """ Attack your enemy using one of three options """
        moves = ['quick', 'normal', 'power', 'exit']
        atk = ''
        clear()
        type_print(f'\tWhat attack?\n\n'
                   f"\t|  {self.green('Quick')}  |  {self.green('Normal')}  |  {self.green('Power')}  |", 20000)
        while atk.lower() not in moves:
            atk = input("\n\n\t\t")
            atk.lower()
            if atk not in moves:
                type_print('\t\tThat is not a move!')
            if atk == 'quick':
                self.player_first(60)
                break
            if atk == 'normal':
                first = randint(0, 1)
                if first:
                    self.player_first(100)
                    break
                if not first:
                    self.enemy_first(100)
                    break
            if atk == 'power':
                self.enemy_first(140)
                break
            if atk == 'exit':
                break

    def do_run(self, *_):
        """ Try to run away! """
        clear()
        type_print(f"\t{choice(self.txt['run'])}")
        type_print('\t.........'), time.sleep(1)
        if randint(0, 100) > 30:
            type_print(f"\t{choice(self.txt['success'])}")
            type_print(f'\t{self._player.name} ran away!')
            time.sleep(3)
            self.leave_combat()
        else:
            type_print(f"\t{choice(self.txt['fail'])}")
            self.damage(self.enemy, self._player, 100)

    def do_item(self, *_):
        """ Use an item! """
        selection = self._bag.show_usable()
        if selection is not None:
            clear()
            self._player.use(selection)
            type_print(f"\t{choice(self.txt['enemy'])}")
            self.damage(self.enemy, self._player, 100)
        else:
            clear()
