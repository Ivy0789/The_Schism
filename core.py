"""
This file holds core game functions
"""
from os import path as p
from os import listdir
from pygame import mixer as mix
from random import random as r
from sys import stdout as st
from time import sleep as s
from os import system as sys
from os import name as nm


def call_ascii(filename):  # art credit see char.py
    """
    Calls ascii images from file
    :param filename: filename .txt file from ./image subdirectory 
    """
    if filename in [i.replace('.txt', '') for i in listdir('image')]:
        with open(p.join("./image", f"{filename}.txt"), "r") as file:
            for line in file:
                print(line.rstrip())
    else:
        with open(p.join("./image", "battle.txt"), "r") as f:
            for ls in f:
                print(ls.rstrip())


# Thanks to SketchyLogic for the audio @ https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles
def call_audio(file, loop=-1):
    """

    Args:
        file: name of file
        loop: whether to loop. -1 is infinite, zero plays only once, ect. defaults to -1
    """
    audio = mix.Sound(p.join("./audio", f"{file}.ogg"))
    audio.play(loops=loop)


def type_print(text: str, speed: int = 1500) -> print:
    """
    Slow typing function
    :param text: "what you want to print out'
    :param speed: integer of words per minute
    """
    for letter in text:
        st.writelines(letter)
        st.flush()
        s(r() * 10.0 / speed)


def clear():  # defines clear screen for lin or win sys.
    """ Clears the screen """
    if nm == 'nt':
        _ = sys('cls')
    else:
        _ = sys('clear')
