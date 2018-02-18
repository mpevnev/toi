"""

Main menu module.

The processor it contains handles the main menu.

"""

import toi.cat as cat
import toi.cat.common as comm
import toi.cat.main_menu as mm
import toi.processor as proc

class Processor(proc.Processor):
    """ Main menu processor. """

    def __init__(self, p):
        super().__init__(p)
        self.has_greeted = False
        # Set up commands.
        self.make_command(self.show_help, cat.C_COMMON, comm.CMD_HELP)
        self.make_command(self.quit, cat.C_COMMON, comm.CMD_QUIT)

    def _run(self):
        if not self.has_greeted:
            self.io.say(self.strings[cat.S_MAIN_MENU][mm.GREETING])
            self.has_greeted = True
        inp = self.io.ask(self.strings[cat.S_MAIN_MENU][mm.PROMPT])
        if inp == "":
            self.io.say(self.strings[cat.S_COMMON][comm.EMPTY_CMD])
            return self
        cmd_res = self.command(inp)
        return self

    def show_help(self, args):
        """ Show help on some topic. """
        pass

    def quit(self, args):
        """ Quit the game. """
        self.io.say(self.strings[cat.S_COMMON][comm.FAREWELL])
        self.io.flush()
        raise proc.NextProcessor(None)
