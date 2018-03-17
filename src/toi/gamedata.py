"""
Game data module.

Provides GameData class used to hold all data of the game - control strings,
normal strings, monster recipes, class recipes, etc.
"""


import toi.cat as cat
from toi.read import read


class GameData():
    """
    A container for game data.
    """

    def __init__(self):
        self.control = _read_control()
        self.strings = _read_strings()
        self.help = _read_help()


def _read_control():
    """ Read game control strings. """
    res = {}
    res[cat.C_COMMON] = read("control", "common.yaml")
    res[cat.C_MAIN_MENU] = read("control", "main_menu.yaml")
    return res


def _read_strings():
    """ Read game strings. """
    res = {}
    res[cat.S_COMMON] = read("strings", "common.yaml")
    res[cat.S_MAIN_MENU] = read("strings", "main_menu.yaml")
    return res


def _read_help():
    """ Read help strings. """
    return NotImplemented