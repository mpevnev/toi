"""
PC module.

Provides PlayerCharacter.
"""


from collections import deque


import toi.cat as cat
import toi.cat.pc as pc
import toi.misc as misc
import toi.stats as stats


class PlayerCharacter():
    """
    Information about a player character.
    """

    def __init__(self, name, species, background):
        self.name = None
        self.aliases = deque()
        self.species = species
        self.background = background
        self.stats = {}
        self._init_stats()
        self.apply_background_modifiers()
        self.set_name(name)

    #--------- background manipulation ---------#

    def apply_background_modifiers(self):
        """ Apply background's modifiers to stats and other things. """
        pass

    def change_background(self, new_bg):
        """ Change the background information and recalculate stats. """
        self._init_stats()
        self.background = new_bg
        self.apply_background_modifiers()


    #--------- species manipulation ---------#

    def change_species(self, species):
        """ Change PC's species. """
        self.species = species
        self._init_stats()
        self.apply_background_modifiers()

    #--------- stat manipulation ---------#

    def _init_stats(self):
        """ Initialize statistics dict. """
        self.stats = self.species.base_stats.copy()

    #--------- information retrieval ---------#

    def short_description(self, strings):
        """ Return a short description of the character. """
        res = strings[cat.PC][pc.SHORT_DESCR]
        return res.format(
            name=self.name,
            species=self.species.shortname,
            bg=self.background.shortname,
            hp=0,
            maxhp=0
            )


    #--------- misc ---------#

    def add_alias(self, alias):
        """ Add an alias for the PC. """
        self.aliases.append(misc.normalize(alias))

    def remove_alias(self, alias):
        """ Remove an alias. """
        self.aliases = deque(filter(lambda a: a != alias, self.aliases))

    def reset_aliases(self):
        """ Reset the aliases list just to defaults. """
        self.aliases.clear()
        self.aliases.append(misc.normalize(self.name.split()[0]))

    def set_name(self, name):
        """ Set the name of the character and add a default alias. """
        if self.name is not None:
            self.remove_alias(misc.normalize(self.name).split()[0])
        alias = name.split()[0]
        self.add_alias(alias)
        self.name = name
