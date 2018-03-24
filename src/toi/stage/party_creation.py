"""
Party creation module.

The flow it contains handles the party generation.
"""


import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.party_creation as party
import toi.gamestate as state
import toi.misc as misc
from toi.parser import make_parser, parse, Capture
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
        res[party.CMD_CHANGE_PARTY_NAME] = make_parser(
            control[party.CMD_CHANGE_PARTY_NAME], self.game)
        res[party.CMD_DELETE] = make_parser(control[party.CMD_DELETE], self.game)
        res[party.CMD_DONE] = make_parser(control[party.CMD_DONE], self.game)
        res[party.CMD_EDIT] = make_parser(control[party.CMD_EDIT], self.game)
        res[party.CMD_OVERVIEW] = make_parser(control[party.CMD_OVERVIEW], self.game)
        res[party.CMD_QUICK_ADD] = make_parser(control[party.CMD_QUICK_ADD], self.game)
        return res

    def welcome_back(self):
        """ Print 'welcome back' message to mark the end of a subflow. """
        self.io.say(self.data.strings[cat.PARTY_CREATION][party.WELCOME_BACK])

    def read_party_name(self):
        """ Read party's name. """
        name = self.io.ask(self.data.strings[cat.PARTY_CREATION][party.NAME_PROMPT])
        return misc.pretty_name(name)

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
            if self.try_change_name(inp):
                continue
            if self.try_delete(inp):
                continue
            if self.try_overview(inp):
                continue
            self.io.say(self.data.strings[cat.COMMON][common.WHAT])

    #--------- actions ---------#

    def try_abort(self, user_input):
        """
        If 'user_input' is an 'abort' command invokation, return to the main
        menu, otherwise return False.
        """
        output = parse(self.game.common_parsers[common.CMD_ABORT], user_input)
        if output is None:
            return False
        import toi.stage.main_menu as mm
        self.io.say(self.data.strings[cat.COMMON][common.OKAY])
        target = mm.MainMenuFlow(self.io, self.data)
        raise mofloc.ChangeFlow(target, mm.FROM_PARTY_CREATION)

    def try_add(self, user_input):
        """
        If 'user_input' is an 'add' command invokation, start a NewChar subflow
        and then return True, otherwise return False.
        """
        output = parse(self.parsers[party.CMD_ADD], user_input)
        if output is None:
            return False
        subflow = charstage.CharCreationFlow(self.io, self.data, self.game)
        mofloc.execute(subflow, charstage.ENTRY)
        self.welcome_back()
        return True

    def try_change_name(self, user_input):
        """
        If 'user_input' is a 'change name' command invokation, change party's
        name, print it out and return True, otherwise return False.
        """
        output = parse(self.parsers[party.CMD_CHANGE_PARTY_NAME], user_input)
        if output is None:
            return False
        name = misc.pretty_name(output[Capture.NAME])
        self.game.party.name = name
        msg = self.data.strings[cat.PARTY_CREATION][party.NEW_NAME_IS]
        msg = msg.format(party_name=name)
        self.io.say(msg)
        return True

    def try_delete(self, user_input):
        """
        If 'user_input' is a 'delete' command invokation, delete the specified
        character from the party and return True, otherwise return False.
        """
        output = parse(self.parsers[party.CMD_DELETE], user_input)
        if output is None:
            return False
        if output[Capture.PC] is None:
            self.io.say(self.data.strings[cat.COMMON][common.NO_SUCH_CHAR])
            return True
        self.game.party.delete_character(output[Capture.PC])
        msg = self.data.strings[cat.PARTY_CREATION][party.DONE_DELETING]
        msg = msg.format(deleted_pc=output[Capture.PC].name)
        self.io.say(msg)
        return True

    def try_overview(self, user_input):
        """
        If 'user_input' is a 'list' command invokation, print party's name and
        short info on each character, then return True, otherwise return False.
        """
        output = parse(self.parsers[party.CMD_OVERVIEW], user_input)
        if output is None:
            return False
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
                self.io.say(prefix, pc.short_description(self.data.strings))
        return True

    def try_quit(self, user_input):
        """
        If 'user_input' is a 'quit' command invokation, quit the game,
        otherwise return False.
        """
        output = parse(self.game.common_parsers[common.CMD_QUIT], user_input)
        if output is None:
            return False
        if self.game.party is None:
            farewell = self.data.strings[cat.COMMON][common.FAREWELL]
        else:
            farewell = self.data.strings[cat.COMMON][common.FAREWELL_WITH_PARTY]
            farewell = farewell.format(party_name=self.game.party.name)
        self.io.say(farewell)
        self.io.flush()
        raise mofloc.EndFlow


#--------- helper things ---------#


class StateWithParty(state.GameState):
    """
    A container for game data and party information.
    """

    def __init__(self, data):
        super().__init__(data)
        self.party = None
