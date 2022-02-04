"""
This contains special sequences, like the title sequence.
"""
from colorama import Fore
from colorama import init

from combat import Combat
from core import clear
from core import call_audio
from core import type_print
from core import call_ascii
from pygame import mixer as m
from time import sleep


def start_sequence():
    init()
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
    name = input()
    Combat.player._name = name
    sleep(1), clear()
    type_print(f'\n\tGreetings, {name}, but Beware...'
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
    type_print(Fore.BLUE + f"\n\n\t{name}" + Fore.YELLOW + "..."
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
               f'\n\t\t... Good luck on your journey, {Fore.BLUE}{name}{Fore.YELLOW}!\n'
               f"\n\t\t Remember, type 'help' if you need help!\n")
    m.fadeout(5000), sleep(3), clear()


def final_sequence():  # todo boss fight
    pass


def skip_start():
    while True:
        #r = input("Enter Y to skip intro\n\t")
        #p = r.upper()
        #if p != "Y":
        #    start_sequence()
        #    break
        #else:
            name = input('Name: ')
            Combat.player._name = name
            clear()
            break
