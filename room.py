"""
This is the room module. It controls room follow and movement in conjugation with the game Engine.
The room system is modular, simply scanning a JSON file with the room data and creating a new Room object.

"""
from os import path as p
import json

from colorama import Fore


def get_room(id):
    """
    This gets the room characteristics for the requested room
    Args:
        id: the id of the room passed from the Engine move method, which mirrors the name of the json file

    Returns: dictionary of values that defines the room as an instance of Room

    """
    with open(p.join("./rooms/", f"{id}.json"), "r", newline='\n') as infile:
        read = infile.read()  # reads whole file into var as byte
        load = json.loads(read)  # deserializes byte read into dict
        load['id'] = id  # specifies args as dict keys
        room_dict = Room(**load)  # ** passes through all kwargs of load.
    return room_dict


class Room:
    def __init__(self, id: int, name: str, description: str, connections: dict,
                 enemy: bool, item: list, instruction: str
                 ):
        self.id = id
        self._name = name
        self._description = description
        self._connections = connections
        self.enemy = bool(enemy)
        self.item = item
        self._instruction = instruction

    def connections(self, direction):
        """

        Args:
            direction:

        Returns: None

        """
        if direction in self._connections:
            return self._connections[direction]
        else:
            pass

    @property
    def name(self):
        return Fore.LIGHTYELLOW_EX + self._name.capitalize() + Fore.YELLOW

    @property
    def instruction(self):
        return self._instruction.replace(
            'North', Fore.LIGHTYELLOW_EX + 'North' + Fore.YELLOW).replace(
            'East', Fore.LIGHTYELLOW_EX + 'East' + Fore.YELLOW).replace(
            'South', Fore.LIGHTYELLOW_EX + 'South' + Fore.YELLOW).replace(
            'West', Fore.LIGHTYELLOW_EX + 'West' + Fore.YELLOW)

    @property
    def description(self):
        return self._description
