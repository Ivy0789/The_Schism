"""
This defines the game engine where the room, inventory, and combat systems are accessed.
"""
import cmd
import pygame.mixer

from colorama import Fore
from combat import Combat
from core import clear, type_print
from item import Bag
from random import randint
from room import get_room
from time import sleep


class Engine(cmd.Cmd):
    prompt = f'\n\n\tEnter a direction or command\n\n\t\t{Fore.RESET}'  # sets the command prompt
    bag = Bag()  # this is also a class attribute, and is an instance of the Bag class in which the inventory resides.
    room_enemy_check = []  # these are class attributes. It is unchanged and cumulative upon each class instance
    room_item_check = []   # These track game progress and halt duplicate combat and duplicate items in rooms.
    equipped = []

    def emptyline(self) -> bool:
        """
        This is a Cmd method. If a cmd line is empty (i.e. user input is empty), onecmd method defaults to this
        method. I override emptyline here because it defaults to lastcmd method, which returns the last entered cmd.
        Therefore, without overriding this method, if a user failed to enter args in response to prompt it would use
        the last entered arg.
        """
        pass

    def preloop(self) -> None:
        """
        This a hook method of Cmd that executes only once as the cmdloop is called. This enables the return from
        combat to give room context rather than a simple prompt.
         """
        self.print_instruction()
        type_print('\n\n\tType help for command list'
                   if self.location.id not in self.room_enemy_check and self.location.id not in self.room_item_check
                   else '')

    def precmd(self, line: str) -> str:
        """
        This method is a hook method of Cmd that executes immediately after input entry, but before command dispatch/
        interpretation. Here, it allows the user entry text to be white and core game txt to be yellow.
        Args:
            line: the user input

        Returns: line

        """
        print(Fore.YELLOW)
        return line

    def postcmd(self, stop: bool, line: str) -> bool:
        """
        This method is a hook method of Cmd that executes immediately after command dispatch. Here, it is overwritten
        to provide the name of the room to the player after each command is given, which effectively means it prints
        before the prompt. It also manages enemy system in relation to cmdloop iteration, generating a roughly 1 in 6
        chance that a fight will randomly occur in any given room in which you have not fought before and an enemy
        exists on every iteration of the loop.

        Args:
            stop (bool): true terminates the cmdloop, false continues the execution
            line (str): the str of the last entered user input
        """
        for item in self.bag.bag:
            if item['sort'] == 'equipable' and item['name'] not in self.equipped:
                self.equipped.append(item['name'])
                Combat.player.use(item)
        if line != 'help' and line != 'status' and line != 'look':
            type_print(f'{Fore.YELLOW}\n\tYou are in {Fore.LIGHTYELLOW_EX}{self.location.name}{Fore.YELLOW}')
        if self.location.enemy is True \
                and self.location.id not in self.room_enemy_check \
                and line != 'help' and line != 'status' and line != 'look':
            print(f'\n\n\t\t{Fore.RED}There is danger here.'
                  f'\n\n\t\tBetter not tarry.{Fore.YELLOW}')
            r = randint(1, 6)
            if r == 3:
                sleep(1)
                self.do_fight()
        return False

    def default(self, line: str) -> bool:
        """ This is a Cmd method that determines what message prints if the prompt entered does not match a command"""
        print("\n\tYou can't do that!")
        return False

    def __init__(self, room=1, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initializes Engine's super class, cmd.Cmd
        print(Fore.YELLOW)
        self.location = get_room(room)
        self.print_description() if self.location.id not in self.room_item_check \
            or self.location.id not in self.room_enemy_check else ''

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
            self.print_description() if self.location.id not in self.room_enemy_check \
                or self.location.id not in self.room_item_check else ''
            self.print_instruction()

    def print_description(self):
        sleep(.2)
        type_print(f'\t{self.location.description}')

    def print_instruction(self):
        sleep(.2)
        type_print(f'\t{self.location.instruction}')

    # do_ cmds - the name of each method sets the in-game command name.
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

    @staticmethod
    def do_help(self, **kwargs):
        """ Get help """
        print(
            f"\n\tGame Commands:\n"
            f"\t\t{'fight'.ljust(8)} - Summon a fight, if you can!\n"
            f"\t\t{'bag'.ljust(8)} - Look in your bag or use an item!\n"
            f"\t\t{'look'.ljust(8)} - Look around you for doors!\n"
            f"\t\t{'search'.ljust(8)} - Look around for items!\n"
            f"\t\t{'status'.ljust(8)} - See your current health, attack, defense, and level!\n"
            f"\t\t{'quit'.ljust(8)} - Quit the game!\n"
            f"\tMove Commands:\n"
            f"\t\t{'north'.ljust(8)} - Move north, if possible\n"
            f"\t\t{'east'.ljust(8)} - Move east, if possible\n"
            f"\t\t{'south'.ljust(8)} - Move south, if possible\n"
            f"\t\t{'west'.ljust(8)} - Move west, if possible\n"
        )

    @staticmethod
    def do_quit():
        """ Quit Game """
        return True

    def do_search(self, *_):
        """ Search for an item """
        sleep(.5)
        type_print("\n\n\t......\n\n\t", 50)
        sleep(1.3)
        if self.location.id in self.room_item_check:
            type_print('\n\n\tYou already did that!\n')
        if self.location.id not in self.room_item_check:
            type_print(
                f"\n\n\tYou found {Fore.GREEN}"
                f"""{f'{Fore.YELLOW} and {Fore.GREEN}'.join(self.location.item)
                if len(self.location.item) > 1 else ''.join(self.location.item)
                if len(self.location.item) == 1 else 'nothing'
                }!\n{Fore.YELLOW}"""
            )
            self.room_item_check.append(self.location.id)
            self.bag.check(self.location.item)

    @staticmethod
    def do_status(*_):
        """ Shows player status """
        print(Combat.player.__str__())

    def do_look(self, *_):
        """ Look around you """
        self.print_instruction()

    def do_fight(self, *_):
        """ To Battle! """
        if self.location.enemy is True and self.location.id not in self.room_enemy_check:
            clear()
            pygame.mixer.fadeout(1000)  # play battle intro music
            type_print('\n\n\tYou sense something is watching you and call out a challenge...'
                       '\n\n\tSuddenly you hear an ominous swirling and feel the air crackle!\n')
            sleep(1.4)
            self.room_enemy_check.append(self.location.id)
            return Combat(bag=self.bag, loc=self.location).cmdloop() and False
        else:
            type_print(f'\n\t\t{Fore.RED}There is no battle here!{Fore.YELLOW}\n')

    def do_bag(self, *_):
        """ See your Bag or use and Item """
        ent = ""
        type_print(f'{Fore.GREEN}\n\t\t  See  or  Use?\n\n{Fore.YELLOW}')
        while ent.lower() != 'see' or ent.lower() != "use":
            ent = input('\t\t\t')
            if ent.lower() == 'see':
                type_print(f"\n\tYou have:\n\t\t|  ")
                for key, value in self.bag.__index__():
                    print(f"\n\t\t|  {Fore.GREEN}{key} {Fore.YELLOW}x{Fore.GREEN} {value}{Fore.YELLOW}", end='\n\t\t')
                print('\n\n\t')
                break
            if ent.lower() == 'use':
                Combat.player.use(self.bag.show())
                break
