"""
Main menu module.

The flow it contains handles the main menu.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.main_menu as mm
import toi.gamestate as state
from toi.parser import make_parser
import toi.stage.common as cstage


FROM_STARTUP = "from startup"
FROM_GAME_PROPER = "from game"


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
        control = self.data.control[cat.MAIN_MENU]
        res[mm.CMD_NEW_GAME] = make_parser(control[mm.CMD_NEW_GAME], self)
        res[mm.CMD_GREET] = make_parser(control[mm.CMD_GREET], self)
        return res

    #--------- entry points ---------#

    def from_startup(self):
        """
        Actions to perform if this flow was entered from the startup flow.
        """
        self.io.say(self.data.strings[cat.MAIN_MENU][mm.GREETING])
        while True:
            inp = self.io.ask(self.data.strings[cat.MAIN_MENU][mm.PROMPT])
            if self.try_help(inp):
                continue
            if self.try_greet(inp):
                continue
            self.try_new_game(inp)
            self.try_quit(inp)
            # wut?
            self.io.say(self.data.strings[cat.COMMON][common.WHAT])

    def from_game_proper(self):
        """
        Actions to perform if the menu was invoked from inside the game.
        """
        raise NotImplementedError

    #--------- menu actions ---------#

    def try_greet(self, user_input):
        """
        If 'user_input' is a 'greet me' command invokation, greet the player
        one more time and return True, otherwise return False.
        """
        p = self.parsers[mm.CMD_GREET]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            self.io.say(self.data.strings[cat.MAIN_MENU][mm.GREETING])
            return True
        return False

    def try_new_game(self, user_input):
        """
        If 'user_input' is a 'new game' command invokation, run the party
        creation flow, otherwise return False.
        """
        new_game_parser = self.parsers[mm.CMD_NEW_GAME]
        output = epp.parse(epp.SRDict(), user_input, new_game_parser)
        if output is not None:
            import toi.stage.party_creation as party
            target_flow = party.PartyCreationFlow(self.io, self.data)
            raise mofloc.ChangeFlow(target_flow, party.FROM_MAIN_MENU)
        return False

    def try_quit(self, user_input):
        """
        If 'user_input' is a 'quit' command invokation, quit the game,
        otherwise return False.
        """
        quit_parser = self.game.common_parsers[common.CMD_QUIT]
        output = epp.parse(epp.SRDict(), user_input, quit_parser)
        if output is not None:
            self.io.say(self.data.strings[cat.COMMON][common.FAREWELL])
            self.io.flush()
            raise mofloc.StopFlow
        return False
