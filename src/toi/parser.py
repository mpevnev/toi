"""
Parser module.

Provides 'make_parser' function to transform strings into parsers.
"""


from collections import deque


import epp


#--------- main function ---------#


def make_parser(alternative_strings, game_state):
    """
    Create and return a parser that will be able to query 'game_state' Game
    object for data and which grammar will be given by 'alternative_strings'.
    """
    alternatives = deque()
    for string in alternative_strings:
        alternatives.append(_make_alternative(string, game_state))
    return epp.branch(alternatives, save_iterator=False)


#--------- helper things ---------#


def _make_alternative(string, game_state):
    """ Create and return a parser from a particular grammar. """
    literal = _make_literal()
    optional = _make_optional(game_state)
    parsers = deque()
    # Note the order - literal goes last because it matches pretty much anything
    white = epp.whitespace(min_num=0)
    piece = epp.chain(
        [white,
         epp.effect(lambda val, st: parsrs.append(white)),
         epp.branch([optional, literal], save_iterator=False),
         epp.effect(lambda val, st: parsers.append(val)),
         epp.effect(lambda val, st: parsers.append(white)),
         white])
    total = epp.many(piece, 1)
    output = epp.parse(None, string, total)
    if output is None:
        raise RuntimeError(f"Failed to construct a parser from: '{string}'")
    return epp.chain(parsers)


def _make_literal():
    """ Make a literal parser. """
    return epp.chain(
        [epp.any_word(),
         epp.effect(lambda val, st: epp.literal(st.parsed))])


def _make_optional(game_state):
    """ Make an optional group parser. """
    return epp.chain(
        [epp.balanced("[", "]"),
         epp.effect(lambda val, st: epp.maybe(_make_alternative(st.parsed, game_state)))])
