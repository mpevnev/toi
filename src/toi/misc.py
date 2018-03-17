"""
Misc module.

Provides functions that don't fit anywhere else.
"""


def normalize(string):
    """ Normalize a string. """
    return "".join(string.lower().split())
