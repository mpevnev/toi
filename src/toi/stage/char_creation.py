"""
Character creation module.

Provides a flow for adding a character to the party.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.char_creation as char
import toi.misc as misc
from toi.parser import make_parser, Capture
from toi.pc import PlayerCharacter
import toi.stage.common as cstage


ENTRY = "the only"


class CharCreationFlow(cstage.FlowWithHelp):
    """ Character creation (and addition to the party) flow. """

    def __init__(self, io, data, game):
        super().__init__(io, data, game)
        self.register_entry_point(ENTRY, self.entry_point)
        self.parsers = self.prepare_parsers()
        self.name = None
        self.background = None
        self.species = None

    #--------- helper things ---------#

    def prepare_parsers(self):
        """ Prepare parsers used in character creation actions. """
        res = {}
        control = self.data.control[cat.CHAR_CREATION]
        res[char.CMD_DONE] = make_parser(control[char.CMD_DONE], self.game)
        res[char.CMD_LIST_BGS] = make_parser(control[char.CMD_LIST_BGS], self.game)
        res[char.CMD_LIST_SPECIES] = make_parser(control[char.CMD_LIST_SPECIES], self.game)
        res[char.CMD_OVERVIEW] = make_parser(control[char.CMD_OVERVIEW], self.game)
        res[char.CMD_SET_BG] = make_parser(control[char.CMD_SET_BG], self.game)
        res[char.CMD_SET_SPECIES] = make_parser(control[char.CMD_SET_SPECIES], self.game)
        return res

    #--------- entry point ---------#

    def entry_point(self):
        """ Create and add a character. """
        self.io.say(self.data.strings[cat.CHAR_CREATION][char.GREETING])
        self.name = self.read_name()
        while True:
            inp = self.io.ask(self.data.strings[cat.CHAR_CREATION][char.PROMPT])
            if self.try_help(inp):
                continue
            if self.try_done(inp):
                continue
            if self.try_list_bgs(inp):
                continue
            if self.try_list_species(inp):
                continue
            if self.try_overview(inp):
                continue
            if self.try_set_bg(inp):
                continue
            if self.try_set_species(inp):
                continue
            self.io.say(self.data.strings[cat.COMMON][common.WHAT])

    #--------- actions ---------#

    def read_name(self):
        """ Read and return the name of the party. """
        while True:
            name = self.io.ask(self.data.strings[cat.CHAR_CREATION][char.NAME_PROMPT])
            name = misc.normalize(name)
            if name == "":
                continue
            return misc.pretty_name(name)

    def try_done(self, user_input):
        """
        If 'user_input' is a 'done' command invokation, add the generated
        character to the party and end the flow.
        Otherwise, return False.
        """
        p = self.parsers[char.CMD_DONE]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            if self.background is None:
                self.io.say(self.data.strings[cat.CHAR_CREATION][char.SELECT_BG])
                return True
            if self.species is None:
                self.io.say(self.data.strings[cat.CHAR_CREATION][char.SELECT_SPECIES])
                return True
            player = PlayerCharacter(self.name, self.species, self.background)
            self.game.party.characters.add_character(player)
            raise mofloc.EndFlow
        return False

    def try_list_bgs(self, user_input):
        """
        If 'user_input' is a 'list bgs' command invokation, list available
        backgrounds and return True, otherwise return False.
        """
        return False

    def try_list_species(self, user_input):
        """
        If 'user_input' is a 'list species' command invokation, list available
        species and return True, otherwise return False.
        """
        return False

    def try_overview(self, user_input):
        """
        If 'user_input' is an 'overview' command invokation, print out an
        overview of the character being created.
        """
        p = self.parsers[char.CMD_OVERVIEW]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            strings = self.data.strings[cat.CHAR_CREATION]
            name_line = strings[char.NAME].format(name=self.name)
            if self.background is None:
                bg_line = strings[char.BG].format(bg=strings[char.NOT_SELECTED])
            else:
                bg_line = "background: temp"
            if self.species is None:
                species_line = strings[char.SPECIES].format(species=strings[char.NOT_SELECTED])
            else:
                species_line = strings[char.SPECIES].format(species=self.species.name)
            self.io.say(name_line)
            self.io.say(bg_line)
            self.io.say(species_line)
            return True
        return False

    def try_set_bg(self, user_input):
        """
        If 'user_input' is a 'set bg' command invokation, set the background of
        the character being created to the value captured by the parser.
        """
        return False

    def try_set_species(self, user_input):
        """
        If 'user_input' is a 'set species' command invokation, set the species
        of the character being created to the value captured by the parser.
        """
        p = self.parsers[char.CMD_SET_SPECIES]
        output = epp.parse(epp.SRDict(), user_input, p)
        if output is not None:
            species = output[0][Capture.SPECIES]
            if species is None:
                self.io.say(self.data.strings[cat.CHAR_CREATION][char.NOT_A_VALID_SPECIES])
                return True
            self.species = species
            return True
        return False
