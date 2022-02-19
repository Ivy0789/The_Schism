"""
This defines the game engine where the room, inventory, and combat systems are accessed.
"""
import cmd
import subprocess
import sys

import colorama
import tabulate

from char import Hero
from colorama import Fore
from combat import Combat
from core import clear
from core import type_print
from core import call_audio
from core import call_music
from core import call_ascii
from item import Bag
from os import listdir
from os import path
from pygame import mixer
from random import randint
from room import get_room
from time import sleep

tabulate.PRESERVE_WHITESPACE = True


def start_sequence():
    """ The opening game sequence """
    clear()
    call_music('pause')
    call_audio("opening")
    sleep(1.1)
    type_print(f"{Fore.YELLOW}\n\t....\n\t....", 150)
    sleep(1.5)
    clear()
    type_print(f'\n\tOh My! Hello!', 150)
    sleep(1.5)
    clear()
    type_print(f"\n\t I didn't see you there!", 150)
    sleep(1.5)
    clear()
    type_print("\n\t....\n\t....", 150)
    sleep(1.5)
    clear()
    type_print(f'\n\tTell me, Traveler,\n\t\tWhat is your '
               f'{Fore.LIGHTBLUE_EX}name{Fore.YELLOW}?\n', 150
               )
    player_name = Fore.LIGHTBLUE_EX + input("\n\t\t") + Fore.YELLOW
    sleep(1), clear()
    type_print(f'\n\tGreetings, {player_name}, but Beware...'
               f'\n\tFor Darkness dwells within this Lair!'
               f'\n\tIf ending Darkness be thy Fight...'
               f'\n\tThen Venture forth and test thy Might!\n', 150
               )
    sleep(2.2)
    clear()
    print(Fore.RED)
    call_ascii("prepare"), sleep(.8)
    call_ascii("to"), sleep(.8)
    call_ascii("enter"), sleep(1.3)
    call_ascii("schism"), sleep(2)
    sleep(2.6)
    clear()
    type_print(f"\n\n\t{player_name}...\n\t"
               f"{Fore.RED}The Dark Schism{Fore.YELLOW} is open again."
               f"\n\tMany Travelers have perished to seal this fel chasm."
               f"\n\tThe legacy of their efforts are strewn about the Keep."
               f"\n\tCollect their haunted armaments and seal the Schism for good!\n", 150
               )
    type_print('\n\tPress Enter to Continue....\t\n'), input("\n\n\t")
    clear()
    type_print("\n\t\tBut don't be hasty, my dear friend." 
               '\n\t\tFor more than ghosts may haunt these bends.'
               '\n\t\tWith purpose, go, but stay your stride'
               '\n\t\tLest you cross a stark surprise!\n', 150
               )
    sleep(3), clear()
    type_print("\n\t\tWAIT!!")
    sleep(1)
    type_print(f'\n\t\tTake this {Fore.GREEN}Potion{Fore.YELLOW}!\n'
               f'\n\t\t... Good luck on your journey, {player_name}!\n'
               f"\n\t\t Remember, type 'help' if you need help!\n", 150)
    mixer.fadeout(5000), sleep(3), clear()
    call_music()
    return player_name


def skip_start():
    """ Provides option to skip intro """
    clear()
    if len(sys.argv) <= 1:
        type_print("\tWelcome to The Schism! You can jump right in and skip the introduction if you'd like!")
        entry = check('Would you like to skip the introduction? y/n')
        player_name = input('\tPlease input you name: ') if entry == 'y' else start_sequence()
    else:
        player_name = sys.argv[1]
    return player_name


def combat_check():
    """ Checks whether the player wants to play with combat enabled, thereby changing victory conditions """
    if len(sys.argv) <= 1:
        type_print("\tOh! One more thing...")
        combat = check("Would you like to play with combat? y/n")
        combat = True if combat == 'y' else False
    else:
        combat = sys.argv[2]
    clear()
    type_print("\tLoading...", 100)
    return combat


def game_over():
    """ Game lost sequence """
    mixer.fadeout(1000)
    call_music('pause')
    call_audio("lose")
    type_print("\tKhakaron's dark army will wreak havoc over the lands!")
    type_print("\tYou lose!")
    sleep(2)
    entry = check()
    if entry == 'n':
        type_print("\tThanks for playing!")
        print(colorama.Style.RESET_ALL)
        sleep(1)
        sys.stdout.flush()
        quit()
    else:
        call_music('pause')
        mixer.fadeout(1000)
        sys.stdout.flush()
        subprocess.call([sys.executable, path.realpath('main.py')])


def victory(player):
    """
    Victory sequence when player achieves whatever conditions are applicable to their gameplay selection (combat/not)
    """
    mixer.fadeout(1000)
    call_music('pause')
    call_audio("win", 0)
    if player.combat:
        type_print(f"\tCongratulations {player.name}!"
                   f"\n\n\tYou defeated Khakaron!")
        type_print('\tThe land is safe from his wicked Darkness and the Schism has been sealed for good!')
        type_print('\tWe are forever in your debt!')
    else:
        type_print("\tYou collected all the items!")
        type_print("\tYou won! Consider trying again, on a harder difficulty!")
    sleep(2)
    call_audio("interlude")
    entry = check()
    if entry == 'n':
        type_print("\tThanks for playing!")
        sleep(2)
        mixer.fadeout(1000)
        sys.stdout.flush()
        quit()
    else:
        call_music('pause')
        mixer.fadeout(1000)
        sys.stdout.flush()
        subprocess.call([sys.executable, path.realpath('main.py')])


def check(prompt='Would you like to play again? Enter Yes or No.'):
    entry = ""
    while entry != 'y' and entry != 'n':
        entry = input(f"\n\n\t{prompt}\n\n\t")
        entry = entry[0].strip().lower() if entry else ""
    return entry


class Engine(cmd.Cmd):
    prompt = '\n\n\tEnter a direction or command\n\n\t\t'  # sets the command prompt
    room_enemy_check = []  # these are class attributes. It is unchanged and cumulative upon each class instance
    room_item_check = [10, 12]  # these track game progress and halt duplicate combat and duplicate items in rooms.

    def __init__(self,
                 player=Hero(
                     name=skip_start(),
                     health=100,
                     max_hp=100,
                     attack=1000,
                     defense=10,
                     level=1,
                     exp=0,
                     combat=combat_check()
                            ),
                 bag=Bag(),
                 room=1,
                 equipped=None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)  # initializes Engine's super class, cmd.Cmd
        if equipped is None:
            equipped = []
        print(Fore.YELLOW)
        clear()
        self.location = get_room(room)
        self._bag = bag
        self._player = player
        self._equipped = equipped
        self.room_context()

    def emptyline(self) -> bool:
        """
        This is a Cmd method. If a cmd line is empty (i.e. user input is empty), onecmd method defaults to this
        method. Without overriding this method, if a user failed to enter input in response to prompt it would use
        the last entered input. Overriding this method ensures that user input is empty after each execution of the
        cmd loop.
        """
        pass

    def preloop(self) -> None:
        """
        This a hook method of Cmd that executes only once as the cmdloop is called. This enables the return from
        combat to give room context rather than a simple prompt.
         """
        self.equip_items()
        type_print(f'\tYou are in {self.location.name}', 1000)
        self.print_instruction()

    def precmd(self, line: str) -> str:
        """
        This method is a hook method of Cmd that executes immediately after input entry, but before command dispatch/
        interpretation. Here, it ensures proper color and sets line to lowercase. It also provides a convenient
        conditional for decision checking in certain situations.
        Args:
            line: the user input from cmdloop()

        Returns: line

        """
        print(Fore.YELLOW)
        if self.location.id == 6 and line.lower() == 'east' and not self._player.combat:
            player_choice = check("\tAre you sure? There is no going back. (Yes/No)")
            if player_choice == 'y':
                return line.lower()
            else:
                type_print('\tBetter to make sure you are prepared!')
                clear()
                line = ""
                return line.lower()
        else:
            return line.lower()

    def postcmd(self, stop: bool, line: str) -> bool:
        """
        This method is a hook method of Cmd that executes immediately after command dispatch. Here, it is overwritten
        to provide the name of the room to the player after each command is given, which effectively means it prints
        before the prompt. It also manages enemy system in relation to cmdloop iteration, generating a roughly 1 in 6
        chance that a fight will randomly occur in any given room in which you have not fought before and an enemy
        exists on every iteration of the loop. Each clause of this method is separated by a single empty line,
        beginning after the first blank line.

        The first clause prints room instructions after each action method dispatch, except for the commands in
        the header list. Thus, typing 'help' only prints help and does not execute room instructions.

        The second clause handles combat; specifically, it adds a random element of danger to each room where
        an enemy is present. During each iteration, if an enemy is present, has not been fought before, and combat
        is enabled (player choice) it will dispatch a fight 1/6 times. Thus, staying in a danger room for more than six
        iterations, except when help or status commands are dispatched, will likely execute an encounter.

        Args:
            stop (bool): true terminates the cmdloop, false continues the execution
            line (str): the str of the last entered user input
        """
        self.equip_items()
        self.room_context()
        self.victory_conditions_no_combat()

        header = ['help', 'status']
        if line != 'help':
            type_print(f'\tYou are in {self.location.name}', 2000)
            self.print_instruction(1000)

        if self.location.enemy \
                and self.location.id not in self.room_enemy_check \
                and line not in header \
                and self._player.combat:
            # sets random encounter for most action methods.
            type_print(f"\t\t{self.red('There is danger here.')}", 1000)
            r = randint(1, 6)
            if r == 3:
                sleep(1)
                self.do_fight()
        return False

    def victory_conditions_no_combat(self):
        """ Manages victory conditions without combat """
        room_list = [int(i.replace('.json', '')) for i in listdir(path.join("assets", "rooms"))]
        if self.location.id == 10 \
                and sorted(self.room_item_check) == sorted(room_list) \
                and not self._player.combat:
            victory(self._player)
        if self.location.id == 10 \
                and sorted(self.room_item_check) != sorted(room_list) \
                and not self._player.combat:
            type_print("\tYou failed to collect the all of the items!")
            game_over()
        return False

    def default(self, line: str) -> bool:
        """ This is a Cmd method that determines what message prints if the prompt entered does not match a command"""
        clear()
        type_print(self.yellow("\tYou can't do that!\n\n"), 1000)
        return False

    def equip_items(self):
        """ Equips equipable items in bag """
        for item in self._bag.bag:
            if item['sort'] == 'equipable' and item not in self._equipped:
                self._equipped.append(item)
                self._player.use(item)

    # enablers
    def move(self, direction):
        """
        sets the new room to the query of available connected rooms
        if the :param direction (input from do_cmds) matches the
        connected room (direction).
        """
        clear()
        new_room = self.location.connections(direction)
        if new_room is None:
            type_print("\n\tYou can't go that way! Try again or type 'help' for help!")
        else:
            self.location = get_room(new_room)

    def room_context(self):
        """ Contextualizes rooms upon re-entry """
        if self.location.id not in self.room_item_check:
            if self._player.combat:
                if self.location.id not in self.room_enemy_check:
                    self.print_description(300)
                else:
                    type_print(self.red("\tYou have done battle here."))
            else:
                self.print_description(300)
        else:
            if self.location.id != 12 and self.location.id != 10:
                type_print(self.yellow("\tYou have looted this room."))
            if self._player.combat:
                if self.location.id in self.room_enemy_check:
                    type_print(self.red("\tYou have done battle here."))

    def print_description(self, speed=250):
        """ Prints room descriptions """
        sleep(.2)
        type_print(f'\t{self.location.description}', speed)

    def print_instruction(self, speed=250):
        """ Prints room instructions """
        sleep(.2)
        type_print(f'\t{self.location.instruction}', speed)

    @staticmethod
    def red(txt):
        """ Turns text red """
        return f"{Fore.RED}{txt}{Fore.YELLOW}"

    @staticmethod
    def blue(txt):
        """ Turns text blue """
        return f"{Fore.LIGHTBLUE_EX}{txt}{Fore.YELLOW}"

    @staticmethod
    def yellow(txt):
        """ Turns text yellow """
        return f"{Fore.LIGHTYELLOW_EX}{txt}{Fore.YELLOW}"

    # Action Methods - the name of each method sets the in-game command name.
        # directionals
    def do_north(self, *_):
        """ Move north """
        self.move("n")

    def do_east(self, *_):
        """ Move east """
        self.move("e")

    def do_south(self, *_):
        """ Move south """
        self.move("s")

    def do_west(self, *_):
        """ Move west """
        self.move("w")

        # game
    def do_help(self, *_):
        """ Get help """
        clear()
        print(
            f"""
            {self.yellow('Game Commands:')}
            \t{'fight'.ljust(8)} - Summon a fight, if you can!
            \t{'bag'.ljust(8)} - Look in your bag or use an item!
            \t{'search'.ljust(8)} - Look around for items!
            \t{'status'.ljust(8)} - See your current health, attack, defense, and level!
            \t{'quit'.ljust(8)} - Quit the game!
            {self.yellow('Move Commands:')}
            \t{'north'.ljust(8)} - Move north, if possible
            \t{'east'.ljust(8)} - Move east, if possible
            \t{'south'.ljust(8)} - Move south, if possible
            \t{'west'.ljust(8)} - Move west, if possible
            """
        )

    def do_quit(self, *_):
        """ Quit Game """
        type_print(self.yellow('\tThanks for playing!'))
        sleep(2)
        clear()
        print(colorama.Style.RESET_ALL)
        quit()

    def do_search(self, *_):
        """ Search for an item """
        clear()
        type_print("\t.....\n"*2, 50)
        sleep(.8)
        clear()
        room_items = [e for e in self.room_item_check if e != 10 and e != 12]
        if self.location.id in room_items:
            type_print('\tYou already did that!')
            sleep(.5)
            clear()
        if self.location.id not in self.room_item_check:
            type_print(
                f"\tYou found {Fore.LIGHTGREEN_EX}"
                f"""{f'{Fore.YELLOW} and {Fore.LIGHTGREEN_EX}'.join(self.location.item)
                if len(self.location.item) > 1 else ''.join(self.location.item)
                if len(self.location.item) == 1 else 'nothing'
                }!{Fore.YELLOW}"""
            )
            self.room_item_check.append(int(self.location.id))
            self._bag.check(self.location.item)

    def do_status(self, *_):
        """ Shows player status """
        clear()
        print(self._player.__str__())

    def do_fight(self, *_):
        """ To Battle! """
        if self.location.enemy is True \
                and self.location.id not in self.room_enemy_check\
                and self._player.combat:
            clear()
            call_music(command='pause')
            call_audio('battle') if self.location.id != 10 else call_audio('boss')
            type_print('\n\n\tYou sense something is watching you and call out a challenge...'
                       '\n\n\tSuddenly you hear an ominous swirling and the air begins to crackle!')
            sleep(1.6)
            self.room_enemy_check.append(int(self.location.id))
            if self.location.id != 10:
                return Combat(
                    player=self._player,
                    bag=self._bag,
                    loc=self.location,
                    boss=False,
                    equipped=self._equipped).cmdloop() and False
            else:
                return Combat(
                    player=self._player,
                    bag=self._bag,
                    loc=self.location,
                    boss=True,
                    equipped=self._equipped).cmdloop() and False
        else:
            type_print(f'\t{Fore.RED}There is no battle here!{Fore.YELLOW}') if self._player.combat \
                else type_print(f'\t{Fore.RED}Combat is disabled!{Fore.YELLOW}')
            sleep(.8)
            clear()

    def do_bag(self, *_):
        """ See your Bag or use and Item """
        clear()
        player_choice = ""
        type_print(f"\t{self.blue('See or Use?')}")
        while player_choice != 'see' or player_choice != "use":
            player_choice = input('\n\t')
            player_choice = player_choice.lower()
            if player_choice == 'see':
                clear()
                type_print(f"\tYou have:\n\n")
                head = ["Item Name", "Quantity", "Description", "Value\n\t"]
                player_inventory = []
                for name, count in self._bag.__index__():
                    for item in self._bag.bag:
                        if item['name'] == name:
                            player_inventory.append([
                                '\t',
                                self.blue(name),
                                self.blue(count),
                                self.yellow(item['description']),
                                self.yellow(item['value'])
                            ])
                print('\t'
                      + tabulate.tabulate(
                        player_inventory,
                        headers=head,
                        numalign="center",
                        stralign="center",
                        tablefmt='plain')
                      )
                break
            if player_choice == 'use':
                clear()
                t = True
                while t:
                    item_selection = self._player.use(self._bag.show_usable())
                    if item_selection != "exit":
                        t = True
                    else:
                        player_choice = 'exit'
                        break
            if player_choice == 'exit':
                break
