"""
Background module.

Provides Background class used to represent player character classes.
"""


import toi.cat.background as cat
import toi.stats as stats


class Background():
    """ A class representing a playable class. """

    def __init__(self, data):
        self.name = _read_name(data)
        self.shortname = _read_shortname(data)
        self.stat_modifiers = _read_stat_modifiers(data)


#--------- helper things ---------#


def _read_name(data):
    """ Read a name from a data dict. """
    return data[cat.NAME]


def _read_shortname(data):
    """ Read a short name from a data dict. """
    return data[cat.SHORTNAME]


def _read_stat_modifiers(data):
    """ Read state modifiers info from a data dict. """
    res = {}
    source_keys = [cat.STR, cat.DEX, cat.INT, cat.SPI, cat.CHA, cat.LUC]
    for target_key, source_key in zip(stats.Stat, source_keys):
        res[target_key] = data.get(source_key, 0)
    return res
