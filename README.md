# The_Schism

 Greetings! Welcome to my readme file, which I wrote to
 accompany my game and assist me in solidifying  my
 understanding of Python concepts, procedures, and syntax.
 As such, it is likely overly detailed and potentially wrong
 in some places (or many?), although I did my best to
 read and comprehend the available documentation.

 Each component of the game has its own sub-heading in this file,
 and most game functions are explained, sans the obviously simple.
 If I get something wrong, let me know!


 ## Game Engine

 Using cmd allows for a terminal based continuous command prompt without writing a bunch of code. It calls on the 
 cmd.Cmd class and utilizes the methods and args within. cmd module documentation can be found 
 @ https://docs.python.org/3/library/cmd.html.

The Engine class inherits methods from its super class, Cmd of the cmd module. This is where room movement and item 
handling is done


## Core Module

The Core module contains various personal functions developed for aesthetics,
fun, or streamlining. These functions are generally applied universally, so I
decided to place them in their own module. These functions should be self-evident.


## Rooms and Movement

Room persistence can be implemented to afford the ability scale and change rooms as needed without modifying code. This uses JSON to create the conditions that will populate the Room class, which is then converted to a nested dictionary. These dictionaries can then be queried to determine location, enemy, item,ect, as the player moves through the rooms. See the supplemental documentation - Room Movement Logic.pdf


## Items & Inventory

Placeholder

## Characters

Placeholder

## Combat

Placeholder

## Seq

This module simply contains some stranger one-off things, like the opening sequence and the final sequence.
