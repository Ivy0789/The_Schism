"""
This defines the game engine where the room, inventory, and combat systems are accessed.
"""
import cmd
import tabulate

from char import Hero
from colorama import Fore
from combat import Combat
from core import clear
from core import type_print
from core import call_audio
from core import call_ascii
from item import Bag
from pygame import mixer
from random import randint
from room import get_room
from time import sleep

tabulate.PRESERVE_WHITESPACE = True


def start_sequence():
    """ The opening game sequence """
    clear()
    call_audio("opening")
    type_print(f'{Fore.YELLOW}\n\tOh! Hello!\n\t....\n\t....'
               f"\n\t I didn't see you there!"
               f"\n\t....\n\t...."
               )
    type_print('\n\tTell me, Traveler,\n\t\tWhat is your'
               + Fore.LIGHTBLUE_EX + ' name' + Fore.YELLOW + '?\n'
               )
    player_name = input()
    sleep(1), clear()
    type_print(f'\n\tGreetings, {player_name}, but Beware...'
               '\n\tFor Darkness dwells within this Lair!'
               '\n\tIf ending Darkness be thy Fight...'
               '\n\tThen Venture forth and test your Might!\n'
               )
    sleep(1.2)
    print(Fore.RED)
    call_ascii("prepare"), sleep(.8)
    call_ascii("to"), sleep(.8)
    call_ascii("enter"), sleep(.8)
    call_ascii("schism"), sleep(2)
    type_print(Fore.BLUE + f"\n\n\t{player_name}" + Fore.YELLOW + "..."
               + Fore.RED + "the Dark Schism " + Fore.YELLOW
               + "is open again."
                 "\n\tMany Travelers have perished to seal this fel chasm."
                 '\n\tThe legacy of their efforts are strewn about the Keep.'
                 "\n\tCollect their haunted armaments and seal the Schism for good!\n"
               )
    type_print('\n\tPress Enter to Continue....\t\n'), input("\n\n\t")
    clear()
    type_print("\n\t\tBut don't be hasty, my dear friend."
               '\n\t\tFor more than ghosts may haunt these bends.'
               '\n\t\tWith purpose, go, but stay your stride'
               '\n\t\tLest you cross a stark surprise!\n'
               )
    sleep(3), clear()
    type_print(f'\n\t\tHere! Take this {Fore.GREEN}Potion{Fore.YELLOW}!'
               f'\n\t\t... Good luck on your journey, {Fore.BLUE}{player_name}{Fore.YELLOW}!\n'
               f"\n\t\t Remember, type 'help' if you need help!\n")
    mixer.fadeout(5000), sleep(3), clear()
    return player_name


def skip_start():
    clear()
    player_name = input('Name: ')
    clear()
    return player_name


class Engine(cmd.Cmd):
    prompt = f'\n\n\tEnter a direction or command\n\n\t\t{Fore.RESET}'  # sets the command prompt
    room_enemy_check = []  # these are class attributes. It is unchanged and cumulative upon each class instance
    room_item_check = []  # These track game progress and halt duplicate combat and duplicate items in rooms.
    equipped = []

    def __init__(self,
                 player=Hero(name=skip_start(),
                             health=100,
                             maxhp=100,
                             attack=10,
                             defense=10,
                             level=1,
                             exp=0),
                 bag=Bag(), room=1, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initializes Engine's super class, cmd.Cmd
        print(Fore.YELLOW)
        self.location = get_room(room)
        self._bag = bag
        self._player = player
        if self.location.id not in self.room_item_check or self.location.id not in self.room_enemy_check:
            self.print_description()

    def emptyline(self) -> bool:
        """
        This is a Cmd method. If a cmd line is empty (i.e. user input is empty), onecmd method defaults to this
        method. Without overriding this method, if a user failed to enter input in response to prompt it would use
        the last entered input.
        """
        pass

    def preloop(self) -> None:
        """
        This a hook method of Cmd that executes only once as the cmdloop is called. This enables the return from
        combat to give room context rather than a simple prompt.
         """
        type_print(f'\tYou are in {self.location.name}', 1000)
        self.print_instruction()
        if self.location.id not in self.room_enemy_check and self.location.id not in self.room_item_check:
            type_print('\tType help for command list')

    def precmd(self, line: str) -> str:
        """
        This method is a hook method of Cmd that executes immediately after input entry, but before command dispatch/
        interpretation. Here, it ensures proper color.
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
        header = ['help', 'status']
        for item in self._bag.bag:
            if item['sort'] == 'equipable' and item['name'] not in self.equipped:
                self.equipped.append(item['name'])
                self._player.use(item)

        if line not in header:
            print(f'\n\tYou are in {self.location.name}')
            self.print_instruction(1000)

        if self.location.enemy is True and self.location.id not in self.room_enemy_check and line not in header:
            print(f'\n\n\t\t{Fore.RED}There is danger here.{Fore.YELLOW}')
            r = randint(1, 6)  # adds random combat element. todo use this to make combat optional at start.
            if r == 3:
                sleep(1)
                self.do_fight()
        return False

    def default(self, line: str) -> bool:
        """ This is a Cmd method that determines what message prints if the prompt entered does not match a command"""
        print("\n\tYou can't do that!")
        sleep(.5)
        clear()
        return False

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
            if self.location.id not in self.room_enemy_check or self.location.id not in self.room_item_check:
                self.print_description()

    def print_description(self, speed=250):
        sleep(.2)
        type_print(f'\t{self.location.description}', speed)

    def print_instruction(self, speed=250):
        sleep(.2)
        type_print(f'\t{self.location.instruction}', speed)

    @staticmethod
    def blue(txt):
        return f"{Fore.LIGHTBLUE_EX}{txt}{Fore.YELLOW}"

    @staticmethod
    def yellow(txt):
        return f"{Fore.LIGHTYELLOW_EX}{txt}{Fore.YELLOW}"

    # Action Commands - the name of each method sets the in-game command name.
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
            f"\t\t{'search'.ljust(8)} - Look around for items!\n"
            f"\t\t{'status'.ljust(8)} - See your current health, attack, defense, and level!\n"
            f"\t\t{'quit'.ljust(8)} - Quit the game!\n"
            f"\tMove Commands:\n"
            f"\t\t{'north'.ljust(8)} - Move north, if possible\n"
            f"\t\t{'east'.ljust(8)} - Move east, if possible\n"
            f"\t\t{'south'.ljust(8)} - Move south, if possible\n"
            f"\t\t{'west'.ljust(8)} - Move west, if possible"
        )

    @staticmethod
    def do_quit():
        """ Quit Game """
        return True

    def do_search(self, *_):
        """ Search for an item """
        clear()
        type_print("\t......", 50)
        sleep(1)
        if self.location.id in self.room_item_check:
            type_print('\n\n\tYou already did that!\n')
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
            self.room_item_check.append(self.location.id)
            self._bag.check(self.location.item)

    def do_status(self, *_):
        """ Shows player status """
        print(self._player.__str__())

    def do_fight(self, *_):
        """ To Battle! """
        if self.location.enemy is True and self.location.id not in self.room_enemy_check:
            clear()
            mixer.fadeout(1000)  # todo play battle intro music
            type_print('\n\n\tYou sense something is watching you and call out a challenge...'
                       '\n\n\tSuddenly you hear an ominous swirling and feel the air crackle!')
            sleep(1.4)
            self.room_enemy_check.append(self.location.id)
            if self.location.id != 10:
                return Combat(player=self._player, bag=self._bag, loc=self.location, boss=False).cmdloop() and False
            else:
                return Combat(player=self._player, bag=self._bag, loc=self.location, boss=True).cmdloop() and False
        else:
            type_print(f'\n\t\t{Fore.RED}There is no battle here!{Fore.YELLOW}\n')
            clear()

    def do_bag(self, *_):
        """ See your Bag or use and Item """
        ent = ""
        print(f"\t\t{self.blue('See or Use?')}")
        while ent != 'see' or ent != "use":
            ent = input('\n\t\t')
            ent = ent.lower()
            if ent == 'see':
                clear()
                type_print(f"\tYou have:\n\n")
                head = ["Item Name", "Quantity", "Description", "Value\n\t"]
                joined = []
                for name, count in self._bag.__index__():
                    for item in self._bag.bag:
                        if item['name'] == name:
                            joined.append(['\t', self.blue(name), self.blue(count),
                                           self.yellow(item['description']), self.yellow(item['value'])])
                print('\t' + tabulate.tabulate(joined, headers=head, numalign="center",
                                               stralign="center", tablefmt='plain'))
                break
            if ent == 'use':
                clear()
                self._player.use(self._bag.show_usable())
                break
