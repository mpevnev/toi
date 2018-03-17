"""
Common stage module.

Provides several functions and classes to handle common interactions like using
help system and asking simple questions.
"""


import epp
import mofloc


import toi.cat.common as common
import toi.parser as parser


#--------- public flow subclasses ---------#


class GameFlow(mofloc.Flow):
    """ A flow that is aware of game data and game state of some sort. """

    def __init__(self, io, data, game):
        super().__init__()
        self.io = io
        self.game = game
        self.data = data


class FlowWithHelp(GameFlow):
    """ A flow that can query game help system. """

    def try_help(self, user_input):
        """
        If 'user_input' is a help command invokation, run the help flow and 
        return True, otherwise do nothing and return False.
        """
        help_parser = self.game.common_parsers[common.CMD_HELP]
        output = epp.parse(epp.SRDict(), user_input, help_parser)
        if output is not None:
            captures = output[0]
            help_flow = _HelpFlow(self.io, self.data, self.game)
            if parser.Capture.TOPIC in captures:
                mofloc.execute(help_flow, HELP_PARTICULAR, captures[parser.Capture.TOPIC])
            else:
                mofloc.execute(help_flow, HELP_GENERAL)
            return True
        return False


#--------- helper flows ---------#


class _HelpFlow(GameFlow):
    """ A flow that queries the game help system. """

    def __init__(self, io, data, game):
        super().__init__(io, data, game)
        self.register_entry_point(HELP_PARTICULAR, self.help_for_topic)
        self.register_entry_point(HELP_GENERAL, self.general_help)

    def help_for_topic(self, topic, exit_after=False):
        """ Display the help for a given topic and then (optionally) exit. """
        raise mofloc.EndFlow

    def general_help(self):
        """ Run interactive help session. """
        raise mofloc.EndFlow


#--------- helper things ---------#

HELP_PARTICULAR = "particular"
HELP_GENERAL = "general"
