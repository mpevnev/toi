"""

Startup module.

The processor it contains loads game data, strings, help etc. and transfers
control to the main menu processor.

"""

import toi.cat as cat
import toi.gameio as gameio
import toi.processor as proc
from toi.read import read
import toi.stage.main_menu as mm

class Processor(proc.Processor):
    """ Startup processor. """

    def __init__(self):
        super().__init__()
        self.data = read_data()
        self.control = read_control()
        self.strings = read_strings()
        self.help = read_help()
        self.io = init_io()
        self.state = init_state()

    def _run(self):
        return mm.Processor(self)

def read_data():
    """ Read game data. """
    return NotImplemented

def read_control():
    """ Read game control strings. """
    res = {}
    res[cat.C_COMMON] = read("control", "common.yaml")
    res[cat.C_MAIN_MENU] = read("control", "main_menu.yaml")
    return res

def read_strings():
    """ Read game strings. """
    res = {}
    res[cat.S_COMMON] = read("strings", "common.yaml")
    res[cat.S_MAIN_MENU] = read("strings", "main_menu.yaml")
    return res

def read_help():
    """ Read help strings. """
    return NotImplemented

def init_io():
    """ Initialize IO object. """
    return gameio.IO()

def init_state():
    """ Initalize game state. """
    return NotImplemented
