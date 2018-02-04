"""

Processor module.

Provides base Processor class for pieces of game logic.

"""

import enum


#--------- base classes ---------#


class Processor():
    """ A piece of game logic. """

    def __init__(self, predecessor=None):
        if predecessor is None:
            self.data = None
            self.control = None
            self.strings = None
            self.help = None
            self.io = None
            self.state = None
        else:
            self.data = predecessor.data
            self.control = predecessor.control
            self.strings = predecessor.strings
            self.help = predecessor.help
            self.io = predecessor.io
            self.state = predecessor.state
        self.commands = {}

    def run(self):
        """ Execute some game flow. """
        try:
            return self._run()
        except StopProcessing as stop:
            return stop.proc

    def command(self, string):
        """
        Execute a command.

        Return a tuple (command, command's return value) if some command was
        executed, or None if no command matched 'words'.
        """
        raise NotImplementedError

    def _run(self):
        """ Execute some game flow. """
        raise NotImplementedError


class StopProcessing(Exception):
    """ An exception to be thrown when a processor exits. """

    def __init__(self, next_proc):
        super().__init__("Uncaught StopProcessing signal")
        self.proc = next_proc
