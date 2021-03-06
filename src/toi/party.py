"""
Party module.

Provides Party class used to hold information about the player's party.
"""


from collections import deque


import toi.misc as misc


class Party():
    """
    A collection of characters and a holder for some party info.
    """

    def __init__(self, name):
        self.name = name
        self.characters = deque()

    #--------- character management ---------#

    def add_character(self, char):
        """ Add a character to the party. """
        self.characters.append(char)

    def delete_character(self, char):
        """ Delete a character from the party. """
        self.characters = deque(filter(lambda c: c is not char, self.characters))
