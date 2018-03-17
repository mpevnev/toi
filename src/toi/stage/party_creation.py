"""
Party creation module.

The flow it contains handles the party generation.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.party_creation as party
import toi.gamestate as state
from toi.parser import make_parser
from toi.party import Party
from toi.pc import PlayerCharacter
import toi.stage.common as cstage


FROM_MAIN_MENU = "from main menu"


class PartyCreationFlow(cstage.FlowWithHelp):
    """
    Party creation flow.
    """

    def __init__(self, io, data):
        super().__init__(io, data, StateWithParty(data))
        self.register_entry_point(FROM_MAIN_MENU, self.from_main_menu)
        self.parsers = self.prepare_parsers()

    #--------- helper things ---------#

    def prepare_parsers(self):
        """ Prepare parsers used in party creation actions. """
        res = {}
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

    #--------- actions ---------#

    def read_party_name(self):
        """ Read party's name. """
        name = self.io.ask(self.data.strings[cat.PARTY_CREATION][party.NAME_PROMPT])
        name = " ".join(map(str.capitalize, name.split()))
        return name


#--------- helper things ---------#


class StateWithParty(state.GameState):
    """
    A container for game data and party information.
    """

    def __init__(self, data):
        super().__init__(data)
        self.party = None
