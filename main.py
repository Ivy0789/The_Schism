"""
This is the game initializer.
"""
# Begin of Command Loop
import os
import pygame
from core import call_audio
from game import Engine
from item import Item
from seq import skip_start

if __name__ == "__main__":
    cmd_size = 'mode 150, 50'
    os.system(cmd_size)  # Sets the cmd window size by cmd_size parameters
    pygame.init()  # initializes the sound module
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512,
        devicename=None,
        allowedchanges=0
    )
    Item().get_item()
    skip_start()
    call_audio("dungeon")
    run = Engine()
    run.cmdloop()
