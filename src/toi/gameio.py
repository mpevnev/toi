"""
IO module.

Provides IO class used to handle user input and output.
"""

from collections import deque
import readline

import toi.cat.io as cat
from toi.read import read


MAX_LINES = 20


class IO():
    """ Input and output handler. """

    def __init__(self):
        self.input = deque()
        self.strings = read("strings", "io.yaml")

    def say(self, *things):
        """ Add a line to the output queue. """
        self.input.append(" ".join(map(str, things)).strip())

    def ask(self, prompt, do_normalize=False):
        """
        Request user input. Return the inputted string, optionally normalized.
        """
        self.flush()
        print()
        inp = input(f"{prompt} ")
        if do_normalize:
            inp = _normalize(inp)
        return inp

    def flush(self):
        """ Print the collected output. """
        i = 0
        for block in self.input:
            for line in block.splitlines():
                print(line)
                i += 1
                if i > MAX_LINES:
                    print(self.strings[cat.CONTINUE])
                    input()
                    i = 0
        self.input.clear()


#--------- helper things ---------#


def _normalize(string):
    """ Normalize a string. """
    return "".join(string.lower().split())
