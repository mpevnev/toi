"""
Party creation module.

The flow it contains handles the party generation.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.party_creation as party
import toi.gamestate as state
import toi.misc as misc
from toi.parser import make_parser
from toi.party import Party
import toi.stage.common as cstage
import toi.stage.char_creation as charstage


FROM_MAIN_MENU = "from main menu"


class PartyCreationFlow(cstage.FlowWithHelp):
    """ Party creation flow. """

    def __init__(self, io, data):
        super().__init__(io, data, StateWithParty(data))
        self.register_entry_point(FROM_MAIN_MENU, self.from_main_menu)
        self.parsers = self.prepare_parsers()

    #--------- helper things ---------#

    def prepare_parsers(self):
        """ Prepare parsers used in party creation actions. """
        res = {}
        control = self.data.control[cat.PARTY_CREATION]
        res[party.CMD_ADD] = make_parser(control[party.CMD_ADD], self.game)
        res[party.CMD_CHANGE_PC_NAME] = make_parser(control[party.CMD_CHANGE_PC_NAME], self.game)
        res[party.CMD_CHANGE_PARTY_NAME] = make_parser(
            control[party.CMD_CHANGE_PARTY_NAME], self.game)
        res[party.CMD_DELETE] = make_parser(control[party.CMD_DELETE], self.game)
        res[party.CMD_EDIT] = make_parser(control[party.CMD_EDIT], self.game)
        res[party.CMD_LIST] = make_parser(control[party.CMD_LIST], self.game)
        return res

    #--------- entry points ---------#

    def from_main_menu(self):
        """
        Actions to perform if this flow is entered from the main menu.
        """
        self.io.say(self.data.strings[cat.PARTY_CREATION][party.GREETING])
        name = self.read_party_name()
        p = Party(name)
        self.game.party = p
        while True:
            inp = self.io.ask(self.data.strings[cat.PARTY_CREATION][party.NEXT])
            # common actions
            self.try_abort(inp)
            if self.try_help(inp):
                continue
            self.try_quit(inp)
            # flow-specific actions
            if self.try_add(inp):
                continue
            if self.try_list(inp):
                continue
            self.io.say(self.data.strings[cat.COMMON][common.WHAT])

    #--------- actions ---------#

    def read_party_name(self):
        """ Read party's name. """
        name = self.io.ask(self.data.strings[cat.PARTY_CREATION][party.NAME_PROMPT])
        return misc.pretty_name(name)

    def try_abort(self, user_input):
        """
        If 'user_input' is an 'abort' command invokation, return to the main
        menu, otherwise return False.
        """
        p = self.game.common_parsers[common.CMD_ABORT]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            import toi.stage.main_menu as mm
            self.io.say(self.data.strings[cat.COMMON][common.OKAY])
            target = mm.MainMenuFlow(self.io, self.data)
            raise mofloc.ChangeFlow(target, mm.FROM_PARTY_CREATION)

    def try_add(self, user_input):
        """
        If 'user_input' is an 'add' command invokation, start a NewChar subflow
        and then return True, otherwise return False.
        """
        p = self.parsers[party.CMD_ADD]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            subflow = charstage.CharCreationFlow(self.io, self.data, self.game)
            mofloc.execute(subflow, charstage.ENTRY)
            return True
        return False

    def try_list(self, user_input):
        """
        If 'user_input' is a 'list' command invokation, print party's name and
        short info on each character, then return True, otherwise return False.
        """
        p = self.parsers[party.CMD_LIST]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            strings = self.data.strings[cat.PARTY_CREATION]
            self.io.say(strings[party.NAME_IS].format(party_name=self.game.party.name))
            try:
                _ = self.game.party.characters[0]
                empty = False
            except IndexError:
                empty = True
            if empty:
                self.io.say(strings[party.EMPTY_PARTY])
            else:
                self.io.say(strings[party.LIST_OF_CHARS])
                for pc in self.game.party.characters:
                    prefix = self.data.strings[cat.COMMON][common.LIST_PREFIX]
                    self.io.say(prefix, pc.short_description())
            return True
        return False

    def try_quit(self, user_input):
        """
        If 'user_input' is a 'quit' command invokation, quit the game,
        otherwise return False.
        """
        quit_parser = self.game.common_parsers[common.CMD_QUIT]
        output = epp.parse(epp.SRDict(), user_input, quit_parser)
        if output is not None:
            if self.game.party is None:
                farewell = self.data.strings[cat.COMMON][common.FAREWELL]
            else:
                farewell = self.data.strings[cat.COMMON][common.FAREWELL_WITH_PARTY]
                farewell = farewell.format(party_name=self.game.party.name)
            self.io.say(farewell)
            self.io.flush()
            raise mofloc.EndFlow
        return False


#--------- helper things ---------#


class StateWithParty(state.GameState):
    """
    A container for game data and party information.
    """

    def __init__(self, data):
        super().__init__(data)
        self.party = None
