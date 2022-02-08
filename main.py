"""
This is the game initializer.
"""
# Begin of Command Loop
import os
import colorama
import pygame
from core import call_audio
from item import Item

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
    import game
    call_audio("dungeon")
    run = game.Engine()
    run.cmdloop()
