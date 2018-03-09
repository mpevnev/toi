"""
Main menu module.

The flow it contains handles the main menu.
"""


import mofloc


import toi.cat as cat
import toi.cat.common as comm
import toi.cat.main_menu as mm


FROM_STARTUP = "from-startup"
FROM_GAME_PROPER = "from-game"


class MainMenuFlow(mofloc.Flow):
    """ Main menu flow. """

    def __init__(self, io, game):
        super().__init__()
        self.register_entry_point(FROM_STARTUP, self.from_startup)
        self.register_entry_point(FROM_GAME_PROPER, self.from_game_proper)
        self.io = io
        self.game = game

    def from_startup(self):
        """
        Actions to perform if this flow was entered from the startup flow.
        """
        self.io.say(self.game.strings[cat.S_MAIN_MENU][mm.GREETING])
        while True:
            inp = self.io.ask(self.game.strings[cat.S_MAIN_MENU][mm.PROMPT])

    def from_game_proper(self):
        """
        Actions to perform if the menu was invoked from inside the game.
        """
        raise NotImplementedError
