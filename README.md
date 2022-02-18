# Requirements

There are several non-standard lib dependencies here.
see requirements.txt for details.

To install requirements, use:

>pip install -r requirements.txt

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

Items are called from file and stored in a protected list against which inventory, ect, can be compared and default item values can be attained. Both Item and Bag are classes against which all item data is tested, with Bag inheriting Item's methods. Bag is then instantiated as an attribute of the Engine, allowing it to be called as needed within the core game functions. This is also passed between Engine and Combat when Combat instantiated/Engine is re-instantiated

## Characters

This class handles player and enemy characters, both of which inherit the methods of Char class, which handles the property getting and setting automatically. This allows combat to be largely automated without extraneous methods detailing how dmg is taken/dealt, as the health property adjusts the requisite object's attribute when a dmg value is passed (e.g, player.health -= x; enemy.health -= x)

## Combat

This is a tag-on module that is optional; players can set combat preference before gameplay begins. If enabled, random combat encounters will occur in dangerous rooms based on number of turns spent in room. A turn is a single loop iteration, thus every command entered without moving rooms increases the risk of encountering an enemy. Enabling combat also changes victory conditions, shifting it from collected items/ entering final room to actually defeating the final boss, regardless of how many items the player collected. It is advisable to collect said items, though, or the final boss fight will likely crush the player. 

## Tests
There are two tests provided, both of which are for the non-combat mode; one executes a lose-game scenario, the other a win-game scenario. Simply run the requisite test and the program will execute automatically, assuming dependencies present and installed. 
Be warned, it will execute too rapidly to read most output and will terminate after final use input at the win/lose conditional. 


## Credits: 

Thanks to @ https://www.opengameart.org contributors for sound fx, including users Sketchy_logic and CelestialGhost, both of whom wished to be mentioned. 

Details can be found in inline comments.