"""
Parser module.

Provides 'make_parser' function to transform strings into parsers.
"""


from collections import deque
import enum


import epp


import toi.misc


#--------- main things ---------#


def make_parser(alternative_strings, game_state):
    """
    Create and return a parser that will be able to query 'game_state' Game
    object for data and which grammar will be given by 'alternative_strings'.
    """
    alternatives = deque()
    for string in alternative_strings:
        alternatives.append(_make_alternative(string, game_state))
    return epp.branch(alternatives, save_iterator=False)


class Capture(enum.Enum):
    """ Keys for groups captured by parsers. """

    TOPIC = enum.auto()


#--------- helper things ---------#


def _make_alternative(string, game_state):
    """ Create and return a parser from a particular grammar. """
    literal = _make_literal()
    optional = _make_optional(game_state)
    topic = _make_topic()
    white = _make_whitespace()
    parsers = deque()
    # Note the order - literal goes last because it matches pretty much anything
    piece = epp.chain(
        [epp.branch(
             [white, 
              optional,
              topic,
              literal], save_iterator=False),
         epp.effect(lambda val, st: parsers.append(val))],
        save_iterator=False)
    total = epp.many(piece, 1)
    output = epp.parse(None, string, total)
    if output is None:
        raise RuntimeError(f"Failed to construct a parser from: '{string}'")
    return epp.chain(parsers)


def _make_literal():
    """ Make a literal parser. """
    predicate = lambda char: char not in ["[", "]", "{", "}"]
    return epp.chain(
        [epp.many(epp.cond_char(predicate), min_hits=1),
         epp.effect(lambda val, st: epp.literal(st.parsed))],
        save_iterator=False)


def _make_optional(game_state):
    """ Make an optional group parser. """
    return epp.chain(
        [epp.balanced("[", "]"),
         epp.effect(lambda val, st: epp.maybe(_make_alternative(st.parsed, game_state)))],
        save_iterator=False)


def _make_topic():
    """ Make a help/apropos topic parser. """
    output_parser = epp.chain(
        [epp.greedy(epp.everything()),
         epp.effect(lambda val, st: val.update({Capture.TOPIC: misc.normalize(st.parsed)}))],
        save_iterator=False)
    return epp.chain(
        [epp.literal("{topic}"),
         epp.effect(lambda val, st: output_parser)],
        save_iterator=False)


def _make_whitespace():
    """ Make a whitespace parser. """
    output_parser = epp.whitespace(min_num=1)
    return epp.chain(
        [epp.whitespace(min_num=1),
         epp.effect(lambda val, st: output_parser)],
         save_iterator=False)
