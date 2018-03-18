"""
PC module.

Provides PlayerCharacter.
"""


import toi.stats as stats


class PlayerCharacter():
    """
    Information about a player character.
    """

    def __init__(self, name, species, background):
        self.name = name
        self.species = species
        self.background = background
        self.stats = {}
        self._init_stats()
        self.apply_background_modifiers()

    #--------- background manipulation ---------#

    def apply_background_modifiers(self):
        """ Apply background's modifiers to stats and other things. """
        pass

    def change_background(self, new_bg):
        """ Change the background information and recalculate stats. """
        self._init_stats()
        self.background = new_bg
        self.apply_background_modifiers()

    #--------- stat manipulation ---------#

    def _init_stats(self):
        """ Initialize statistics dict. """
        self.stats = self.species.base_stats.copy()
