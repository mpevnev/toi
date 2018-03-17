"""
Main menu module.

The flow it contains handles the main menu.
"""


import epp
import mofloc


import toi.cat as cat
import toi.cat.common as comm
import toi.cat.main_menu as mm
import toi.parser as parser


FROM_STARTUP = "from-startup"
FROM_GAME_PROPER = "from-game"


class MainMenuFlow(mofloc.Flow):
    """ Main menu flow. """

    def __init__(self, io, data):
        super().__init__()
        self.register_entry_point(FROM_STARTUP, self.from_startup)
        self.register_entry_point(FROM_GAME_PROPER, self.from_game_proper)
        self.io = io
        self.data = data

    def from_startup(self):
        """
        Actions to perform if this flow was entered from the startup flow.
        """
        self.io.say(self.data.strings[cat.S_MAIN_MENU][mm.GREETING])
        help_source = self.data.control[cat.C_COMMON][comm.CMD_HELP]
        help_parser = parser.make_parser(help_source, None)
        while True:
            inp = self.io.ask(self.data.strings[cat.S_MAIN_MENU][mm.PROMPT])
            output = epp.parse(epp.SRDict(), inp, help_parser)
            if output is not None:
                value = output[0]
                self.io.say(f"Help requested for topic '{value[parser.Capture.TOPIC]}'")


    def from_game_proper(self):
        """
        Actions to perform if the menu was invoked from inside the game.
        """
        raise NotImplementedError
