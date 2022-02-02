When contemplating a game interface, the need for something robust yet flexible yields a desire for something beyond while loops. There are several built-in options for command prompts, and the first that came to mind is the simple cmd line interface used to build those little turtle games so long ago. The Cmd class of the cmd module in the common library provides an excellent framework on which to build. The common docs have more details on this class and the methods therein, which pass some powerful functionality. Cmd has a method cmdloop, which handles a continuous prompt until a True value is returned to the onecmd method, which is the method that interprets the user input. Thus, the Schism’s command line interface was born. 

## Items:
>There are several items in the game. Fourteen can be found in various rooms, the remaining are only accessible through the combat system. As of this writing, there are nineteen total items in the stable alpha build. Items are as follows:

### Findable
- | Apple | Armor | Salted Pork |  Ornate Greaves |
- | Bucket of Water | Chitinous Gauntlets | Dusty Book |
- | Tome of Power | Feather | Salted Pork | Boots |
- | Potion | Orb of Con-Creet | Sword | Palantir |

### Lootable
- | Goblin Helm | Great Axe | Royal Pauldrons | Light of Elune |
- | Mithril Chainmail |

## Rooms:
>There are several rooms contained within a modular system built on JSON dictionaries. This affords an easy way to add more rooms without modifying code. As of this writing, there are 12 rooms in the stable alpha build. Please see the supplemental Game Map.pdf. Rooms are as follows:

1. The Culvert
2. The Storeroom
3. The Guardhouse
4. The Armory
5. The Rookery
6. The Wizard’s Library
7. The Secret Passage
8. The Chapel
9. The Shattered Tower
10. The Schism
11. The Great Hall
12. The Dark Passage


