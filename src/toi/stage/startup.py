"""
Startup module.

The flow it contains loads game data, strings, help etc. and transfers control
to the main menu flow.
"""


import mofloc


from toi.game import Game
import toi.gameio as gameio
import toi.stage.main_menu as mm


ENTRY_POINT = "the-only"


class StartupFlow(mofloc.Flow):
    """ Startup program flow. """

    def __init__(self):
        super().__init__()
        self.register_entry_point(ENTRY_POINT, _start)


def _start():
    """ Perform the setup. """
    game = Game()
    io = _init_io()
    next_flow = mm.MainMenuFlow(io, game)
    raise mofloc.ChangeFlow(next_flow, mm.FROM_STARTUP)


def _init_io():
    """ Initialize IO object. """
    return gameio.IO()
