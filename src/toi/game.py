"""
Game state module.

Provides Game class used to hold all info about the game - data, control
strings, normal strings, etc.
"""


import toi.cat as cat
from toi.read import read


class Game():
    """
    A container for game information.
    """

    def __init__(self):
        self.data = _read_data()
        self.control = _read_control()
        self.strings = _read_strings()
        self.help = _read_help()


def _read_data():
    """ Read game data. """
    return NotImplemented


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
