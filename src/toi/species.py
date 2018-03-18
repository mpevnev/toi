"""
Species module.

Provides Species class.
"""


import toi.cat.species as cat
import toi.stats as stats


class Species():
    """ A class representing playable species. """

    def __init__(self, data):
        self.name = _read_name(data)
        self.shortname = _read_shortname(data)
        self.base_stats = _read_base_stats(data)


#--------- helper things ---------#


def _read_base_stats(data):
    """ Read base statistics for a species from a dictionary. """
    res = {}
    source_keys = [cat.STR, cat.DEX, cat.INT, cat.SPI, cat.CHA, cat.LUC]
    for target_key, source_key in zip(stats.Stat, source_keys):
        res[target_key] = data[source_key]
    return res


def _read_name(data):
    """ Read species name from a dictionary. """
    return data[cat.NAME]


def _read_shortname(data):
    """ Read species short name from a dictionary. """
    return data[cat.SHORTNAME]
