"""
Misc module.

Provides functions that don't fit anywhere else.
"""


def normalize(string):
    """ Normalize a string. """
    return "".join(string.lower().split())


def pretty_name(string):
    """ Make a name pretty: strip the whitespace and capitalize each word. """
    return " ".join(map(str.capitalize, string.split()))
