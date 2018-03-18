"""
Game data module.

Provides GameData class used to hold all data of the game - control strings,
normal strings, monster recipes, class recipes, etc.
"""


import toi.cat as cat
from toi.read import read
import toi.species as species


class GameData():
    """
    A container for game data.
    """

    def __init__(self):
        self.backgrounds = _read_backgrounds()
        self.control = _read_control()
        self.help = _read_help()
        self.species = _read_species()
        self.strings = _read_strings()


def _read_backgrounds():
    """ Read backgrounds data. """
    return NotImplemented


def _read_control():
    """ Read game control strings. """
    res = {}
    res[cat.COMMON] = read("control", "common.yaml")
    res[cat.MAIN_MENU] = read("control", "main_menu.yaml")
    res[cat.PARTY_CREATION] = read("control", "party_creation.yaml")
    return res


def _read_help():
    """ Read help strings. """
    return NotImplemented


def _read_species():
    """ Read species data. """
    return list(map(lambda data: species.Species(data), read("data", "species.yaml")))


def _read_strings():
    """ Read game strings. """
    res = {}
    res[cat.COMMON] = read("strings", "common.yaml")
    res[cat.MAIN_MENU] = read("strings", "main_menu.yaml")
    res[cat.PARTY_CREATION] = read("strings", "party_creation.yaml")
    return res
