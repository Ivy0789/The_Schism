"""
This file holds basic game functions utilized throughout the modules
"""
from os import path
from os import listdir
from pygame import mixer
from random import random
from sys import stdout
from time import sleep
from os import system
from os import name


def call_ascii(filename):  # art credit see char.py
    """
    Calls ascii images from file
    :param filename: filename .txt file from ./image subdirectory 
    """
    if filename in [i.replace('.txt', '') for i in listdir(path.join('assets', 'image'))]:
        with open(path.join("assets", "image", f"{filename}.txt"), "r") as file:
            for line in file:
                print(line.rstrip())
    else:
        with open(path.join("assets", "image", "battle.txt"), "r") as f:
            for ls in f:
                print(ls.rstrip())


# Thanks to SketchyLogic for the audio @ https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles
def call_audio(file, loop=-1):
    """

    Args:
        file: name of file
        loop: whether to loop. -1 is infinite, zero plays only once, ect. defaults to -1
    """
    audio = mixer.Sound(path.join("assets", "audio", f"{file}.ogg"))
    audio.play(loops=loop)


def call_music(command='', loop=-1):
    mixer.music.load(path.join('assets', 'audio', 'dungeon.ogg'))
    if command == 'pause':
        mixer.music.pause()
    else:
        mixer.music.play(loops=loop)


def type_print(text: str, speed: int = 250) -> print:
    """
    Slow typing function
    :param text: "what you want to print out'
    :param speed: integer of words per minute
    """
    print("\n\n\t\t")
    for letter in text:
        stdout.writelines(letter)
        stdout.flush()
        sleep(random() * 10.0 / speed)


def clear():  # defines clear screen for lin or win sys.
    """ Clears the screen """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
