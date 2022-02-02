# The_Schism

 Greetings! Welcome to my game, which I wrote to solidify  my
 understanding of Python. This file is a work in process, but each module will eventually have basic documentation here.
Until then, placeholders will have to do! 


 ## Game Engine

 Using cmd allows for a terminal based continuous command prompt without writing a bunch of code. It calls on the 
 cmd.Cmd class and utilizes the methods and args within. cmd module documentation can be found 
 @ https://docs.python.org/3/library/cmd.html.

The Engine class inherits methods from its super class, Cmd of the cmd module. This is where room movement and item 
handling is done


## Core

The Core module contains various personal functions developed for aesthetics,
fun, or streamlining. These functions are generally applied universally, so I
decided to place them in their own module. These functions should be self-evident.


## Rooms and Movement

Room persistence can be implemented to afford the ability scale and change rooms as needed without modifying code. The Schism uses JSON files, each named with the room number and each containing a dictionary of room values. The JSON is loaded from file, then matched against the Room class and returned as an object that can be queried to determine location, enemy, item,ect, as the player moves through the rooms. See the supplemental documentation - Room Movement Logic.pdf


## Items & Inventory

Placeholder

## Characters

Placeholder

## Combat

Placeholder

## Seq

This module simply contains some stranger one-off things, like the opening sequence and the final sequence.