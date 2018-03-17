"""
Main menu module.

The flow it contains handles the main menu.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.main_menu as mm
import toi.gamestate as state
from toi.parser import make_parser
import toi.stage.common as cstage


FROM_STARTUP = "from-startup"
FROM_GAME_PROPER = "from-game"


class MainMenuFlow(cstage.FlowWithHelp):
    """ Main menu flow. """

    def __init__(self, io, data):
        super().__init__(io, data, state.GameState(data))
        self.register_entry_point(FROM_STARTUP, self.from_startup)
        self.register_entry_point(FROM_GAME_PROPER, self.from_game_proper)
        self.parsers = self.prepare_parsers()

    #--------- helper things ---------#

    def prepare_parsers(self):
        """ Prepare user input parsers. """
        res = {}
        control = self.data.control[cat.C_MAIN_MENU]
        res[mm.CMD_NEW_GAME] = make_parser(control[mm.CMD_NEW_GAME], self)
        res[mm.CMD_GREET] = make_parser(control[mm.CMD_GREET], self)
        return res

    #--------- entry points ---------#

    def from_startup(self):
        """
        Actions to perform if this flow was entered from the startup flow.
        """
        self.io.say(self.data.strings[cat.S_MAIN_MENU][mm.GREETING])
        while True:
            inp = self.io.ask(self.data.strings[cat.S_MAIN_MENU][mm.PROMPT])
            if self.try_help(inp):
                continue
            self.try_new_game(inp)

    def from_game_proper(self):
        """
        Actions to perform if the menu was invoked from inside the game.
        """
        raise NotImplementedError

    #--------- menu actions ---------#

    def try_new_game(self, user_input):
        """
        If 'user_input' is a 'new game' command invokation, run the party
        creation flow, otherwise return False.
        """
        return False
