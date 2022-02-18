"""
This initializes all necessary dependencies when game starts,
sets cmd window parameters, then begins the cmdloop
"""
# Begin of Command Loop
import os
import sys
import colorama
import pygame
from core import call_music
from item import Item


def tests(enable, file_name):
    if enable:
        sys.argv += 'my_name', False
        with open(os.path.join("assets", "tests", f"{file_name}")) as file:
            file = file.readlines()
        return file


if __name__ == "__main__":
    cmd_size = 'mode 150, 50'
    os.system(cmd_size)  # Sets the cmd window size by cmd_size parameters
    pygame.init()
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512,
        devicename=None,
        allowedchanges=0
    )  # initializes the sound module
    colorama.init()
    Item().get_item()
    call_music()
    test_list = ["no_combat_lose.txt", "no_combat_win.txt"]
    queue = tests(True, test_list[1])  # Mostly automated. True to test else False
    print(sys.argv)
    import game
    run = game.Engine()
    run.cmdqueue = queue
    run.cmdloop()
