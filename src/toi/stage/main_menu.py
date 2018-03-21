"""
Main menu module.

The flow it contains handles the main menu.
"""


import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.main_menu as mm
import toi.gamestate as state
from toi.parser import make_parser, parse
import toi.stage.common as cstage


FROM_GAME_PROPER = "from game"
FROM_PARTY_CREATION = "from party creation"
FROM_STARTUP = "from startup"


class MainMenuFlow(cstage.FlowWithHelp):
    """ Main menu flow. """

    def __init__(self, io, data):
        super().__init__(io, data, state.GameState(data))
        self.register_entry_point(FROM_GAME_PROPER, self.from_game_proper)
        self.register_entry_point(FROM_PARTY_CREATION, self.from_party_creation)
        self.register_entry_point(FROM_STARTUP, self.from_startup)
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

    def from_game_proper(self):
        """
        Actions to perform if the menu was invoked from inside the game.
        """
        raise NotImplementedError

    def from_party_creation(self):
        """
        Actions to perform if the menu was entered from the party creation
        menu.
        """
        self.io.say(self.data.strings[cat.MAIN_MENU][mm.WELCOME_BACK])
        self.main_loop()

    def from_startup(self):
        """
        Actions to perform if this flow was entered from the startup flow.
        """
        self.io.say(self.data.strings[cat.MAIN_MENU][mm.GREETING])
        self.main_loop()

    def main_loop(self):
        """ Main processing loop. """
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

    #--------- menu actions ---------#

    def try_greet(self, user_input):
        """
        If 'user_input' is a 'greet me' command invokation, greet the player
        one more time and return True, otherwise return False.
        """
        output = parse(self.parsers[mm.CMD_GREET], user_input)
        if output is None:
            return False
        self.io.say(self.data.strings[cat.MAIN_MENU][mm.GREETING])
        return True

    def try_new_game(self, user_input):
        """
        If 'user_input' is a 'new game' command invokation, run the party
        creation flow, otherwise return False.
        """
        output = parse(self.parsers[mm.CMD_NEW_GAME], user_input)
        if output is None:
            return False
        import toi.stage.party_creation as party
        target_flow = party.PartyCreationFlow(self.io, self.data)
        raise mofloc.ChangeFlow(target_flow, party.FROM_MAIN_MENU)

    def try_quit(self, user_input):
        """
        If 'user_input' is a 'quit' command invokation, quit the game,
        otherwise return False.
        """
        output = parse(self.game.common_parsers[common.CMD_QUIT], user_input)
        if output is None:
            return False
        self.io.say(self.data.strings[cat.COMMON][common.FAREWELL])
        self.io.flush()
        raise mofloc.EndFlow
