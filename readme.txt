 Greetings! Welcome to my readme file, which I wrote to
 accompany my game and assist me in solidifying  my
 understanding of Python concepts, procedures, and syntax.
 As such, it is likely overly detailed and potentially wrong
 in some places (or many?), although I did my best to
 read and comprehend the available documentation.

 Each component of the game has its own sub-heading in this file,
 and most game functions are explained, sans the obviously simple.
 If I get something wrong, let me know!


 ## Engine

 Using cmd allows for a terminal based continuous command
 prompt without writing a bunch of code.
 It calls on the cmd.Cmd class and utilizes the methods and args
 within. cmd module documentation can be found
 @ https://docs.python.org/3/library/cmd.html.

 The class Engine is the game engine. The () after Engine
 contains 'cmd.Cmd' from the cmd module, which designates it
 as the superclass of Engine. This allows Engine to inherit
 all the methods of this superclass, as linked above. These
 methods include cmd.cmdloop, which repeatedly issues a prompt,
 accepts input, parses input, and dispatches it to various
 methods, then passes the remainder as an argument. This
 is used to pass the entry to the do_ methods of the Engine
 class, which returns parsed data to the move method,
 allowing the player to move from room to room.

 cmd.Cmd.__init__ initializes that prompt as an object of Engine
 that both accepts and passes all arguments in and out of the
 command loop. The methods within Engine are part of a continuous
 check system that interprets all system input. It is best thought
 of as a standalone class that only measures and parses input.
 An additional advantage to this method is that it utilizes the built-
 in help function and returns docstrings of methods in the Engine
 as output when help is queried.

The move method sets the variable 'new_room' to the location
returned by _get_connections in the Room class of room.py.
The '_' before 'get_connections' is an identifier phenomenon
called private name mangling. See documentation under 6.2.1
@ https://docs.python.org/3/reference/expressions.html.
This seems to be an unorthodox way to use these identifiers,
but it allows for the calling of _connections without specifying
or importing the class each time.

## Persistent Rooms

Room persistence can be implemented to afford the ability scale
and change rooms as needed without modifying code.
This uses JSON to create the conditions that will
populate the Room class, which is then converted to a nested
dictionary. These dictionaries can then be queried to determine
location, enemy, item,ect, as the player moves through the rooms.

The driving components are in room.py. There, json file are opened
based on the passed argument, id, which is passed by the 'move' method
in the class 'Engine'. This method first asks _connections in
the class 'Room' if the passed argument from the _do directionals
equals the 'connections' dict in the current room (self.location._connections)

If _connections returns nothing, new_room is set to nothing and the
subsequent if branch is executed, repeating the query process. If it returns
the directions that match both the user input and the connections in the
current room, then the new_room is set by engaging the 'get_room' function
in room.py.

## Combat

So this makes sense now. Sort of. The @ decorator,
in this case, turns this method into a 'setter' or
its property decorator. This can be used to link
methods of the same name together in a frictionless
way. So, @property sets a method as the property
@method_name.setter/.deleter/.getter can be applied
to methods of the same name. Those can then modify the
@property method. Critically, in the initialized class
the corresponding attribute should be set to self._namehere.
This creates a private variable (or method) that is modified
by the @property/set/get/del connections. This allows for
a lot of automation with minimal code?

## Core Module

The Core module contains various personal functions developed for aesthetics,
fun, or streamlining. These functions are generally applied universally, so I
decided to place them in their own module.

slow_type_x:
    These function take 10 times a random float between 0 & 1
    divided by the set typing_speed. The print output
    of each letter in a statement calling this function is
    delayed by the resultant float

## Items & Inventory

 The item.py file contains the Item and Inventory classes and handles the bulk of the item system.

    get_item:
        this function fetches the item data from json for a specified list of items if the value
        in the list is present in the item subdirectory. If the item name is not present, it randomly selects
        an item from the dir.

