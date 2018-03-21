"""
Character creation module.

Provides a flow for adding a character to the party.
"""


import mofloc


import toi.cat as cat
import toi.cat.common as common
import toi.cat.char_creation as char
import toi.misc as misc
from toi.parser import make_parser, Capture, parse
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

    def overview(self):
        """ Return the overview string. """
        strings = self.data.strings[cat.CHAR_CREATION]
        name_line = strings[char.NAME].format(name=self.name)
        if self.background is None:
            bg_line = strings[char.BG].format(bg=strings[char.NOT_SELECTED])
        else:
            bg_line = strings[char.BG].format(bg=self.background.name)
        if self.species is None:
            species_line = strings[char.SPECIES].format(species=strings[char.NOT_SELECTED])
        else:
            species_line = strings[char.SPECIES].format(species=self.species.name)
        return "\n".join([name_line, species_line, bg_line])

    #--------- entry point ---------#

    def entry_point(self):
        """ Create and add a character. """
        self.io.say(self.data.strings[cat.CHAR_CREATION][char.GREETING])
        self.name = self.read_name()
        while True:
            inp = self.io.ask(self.data.strings[cat.CHAR_CREATION][char.PROMPT])
            if self.try_help(inp):
                continue
            self.try_abort(inp)
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

    def try_abort(self, user_input):
        """
        If 'user_input' is an 'abort' command invokation, end the flow.
        Otherwise return False.
        """
        output = parse(self.game.common_parsers[common.CMD_ABORT], user_input)
        if output is None:
            return False
        self.io.say(self.data.strings[cat.COMMON][common.OKAY])
        raise mofloc.EndFlow

    def try_done(self, user_input):
        """
        If 'user_input' is a 'done' command invokation, add the generated
        character to the party and end the flow - if the information is
        complete and background and species were selected. If some info is
        missing, say so and return True.

        Otherwise, return False.
        """
        output = parse(self.parsers[char.CMD_DONE], user_input)
        if output is None:
            return False
        if self.background is None:
            self.io.say(self.data.strings[cat.CHAR_CREATION][char.SELECT_BG])
            return True
        if self.species is None:
            self.io.say(self.data.strings[cat.CHAR_CREATION][char.SELECT_SPECIES])
            return True
        prompt = self.data.strings[cat.CHAR_CREATION][char.IS_OK_PROMPT]
        prompt = prompt.format(overview=self.overview())
        response = cstage.yesno(
            prompt,
            self.data.strings[cat.COMMON][common.JUST_YESNO],
            self.game.common_parsers,
            self.io)
        if response is cstage.Response.NO:
            return True
        player = PlayerCharacter(self.name, self.species, self.background)
        self.game.party.add_character(player)
        raise mofloc.EndFlow

    def try_list_bgs(self, user_input):
        """
        If 'user_input' is a 'list bgs' command invokation, list available
        backgrounds and return True, otherwise return False.
        """
        output = parse(self.parsers[char.CMD_LIST_BGS], user_input)
        if output is None:
            return False
        for bg in self.data.backgrounds:
            prefix = self.data.strings[cat.COMMON][common.LIST_PREFIX]
            self.io.say(prefix, bg.name)
        return True

    def try_list_species(self, user_input):
        """
        If 'user_input' is a 'list species' command invokation, list available
        species and return True, otherwise return False.
        """
        output = parse(self.parsers[char.CMD_LIST_SPECIES], user_input)
        if output is None:
            return False
        for species in self.data.species:
            prefix = self.data.strings[cat.COMMON][common.LIST_PREFIX]
            self.io.say(prefix, species.name)
        return True

    def try_overview(self, user_input):
        """
        If 'user_input' is an 'overview' command invokation, print out an
        overview of the character being created.
        """
        output = parse(self.parsers[char.CMD_OVERVIEW], user_input)
        if output is None:
            return False
        self.io.say(self.overview())
        return True

    def try_set_bg(self, user_input):
        """
        If 'user_input' is a 'set bg' command invokation, set the background of
        the character being created to the value captured by the parser.
        """
        output = parse(self.parsers[char.CMD_SET_BG], user_input)
        if output is None:
            return False
        bg = output[0][Capture.BACKGROUND]
        if bg is None:
            self.io.say(self.data.strings[cat.CHAR_CREATION][char.NOT_A_VALID_BG])
            return True
        self.background = bg
        return True

    def try_set_species(self, user_input):
        """
        If 'user_input' is a 'set species' command invokation, set the species
        of the character being created to the value captured by the parser.
        """
        output = parse(self.parsers[char.CMD_SET_SPECIES], user_input)
        if output is None:
            return False
        species = output[0][Capture.SPECIES]
        if species is None:
            self.io.say(self.data.strings[cat.CHAR_CREATION][char.NOT_A_VALID_SPECIES])
            return True
        self.species = species
        return True
