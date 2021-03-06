"""
Parser module.

Provides 'make_parser' function to transform strings into parsers.
"""


from collections import deque
import enum
from itertools import chain


import epp


import toi.misc as misc


#--------- main things ---------#


def make_parser(alternative_strings, game):
    """
    Create and return a parser that will be able to query 'game' GameState
    object for data and which grammar will be given by 'alternative_strings'.
    """
    alternatives = deque()
    for string in alternative_strings:
        alternatives.append(_make_alternative(string, game))
    return epp.branch(alternatives, save_iterator=False)


def parse(parser, inp):
    """
    Use a given parser on a given input string, return a SRDict on success,
    None on failure.
    """
    output = epp.parse(epp.SRDict(), inp, parser)
    if output is None:
        return None
    return output[0]


class Capture(enum.Enum):
    """ Keys for groups captured by parsers. """

    BACKGROUND = enum.auto()
    NAME = enum.auto()
    PC = enum.auto()
    SPECIES = enum.auto()
    TOPIC = enum.auto()


#--------- helper things ---------#


def _make_alternative(string, game, require_eoi=True):
    """ Create and return a parser from a particular grammar. """
    white = _make_whitespace()
    literal = _make_literal()
    optional = _make_optional(game)
    # capturing parsers
    bg = _make_bg(game)
    name = _make_name()
    pc = _make_pc(game)
    species = _make_species(game)
    topic = _make_topic()
    #
    parsers = deque()
    piece = epp.chain(
        [epp.branch(
            [# generic
                white,
                optional,
                literal,
                # captures
                bg,
                name,
                pc,
                species,
                topic
            ], save_iterator=False),
         epp.effect(lambda val, st: parsers.append(val))],
        save_iterator=False)
    total = epp.many(piece, 1)
    output = epp.parse(None, string, total)
    if output is None:
        raise RuntimeError(f"Failed to construct a parser from: '{string}'")
    if require_eoi:
        parsers.append(epp.end_of_input())
    return epp.chain(parsers)


#--------- non-capturing parser generators ---------#

def _make_literal():
    """ Make a literal parser. """
    predicate = lambda char: char not in ["[", "]", "{", "}"]
    return epp.chain(
        [epp.many(epp.cond_char(predicate), min_hits=1),
         epp.effect(lambda val, st: epp.literal(st.parsed))],
        save_iterator=False)


def _make_optional(game):
    """ Make an optional group parser. """
    return epp.chain(
        [epp.balanced("[", "]"),
         epp.effect(lambda val, st: epp.maybe(_make_alternative(st.parsed, game, False)))],
        save_iterator=False)


def _make_whitespace():
    """ Make a whitespace parser. """
    output_parser = epp.whitespace(min_num=1)
    return epp.chain(
        [epp.whitespace(min_num=1),
         epp.effect(lambda val, st: output_parser)],
        save_iterator=False)


#--------- capturing parser generators ---------#


def _make_bg(game):
    """ Make a background parser. """
    def variant(bg):
        """ Make a parser for the background. """
        fullname = epp.literal(misc.normalize(bg.name))
        shortname = epp.literal(misc.normalize(bg.shortname))
        eff = epp.effect(lambda val, st: val.update({Capture.BACKGROUND: bg}))
        return epp.chain(
            [epp.branch([fullname, shortname], save_iterator=False),
             eff],
            save_iterator=False)
    catchall = epp.chain(
        [epp.greedy(epp.everything()),
         epp.effect(lambda val, st: val.update({Capture.BACKGROUND: None}))],
        save_iterator=False)
    total = chain(map(variant, game.data.backgrounds), [catchall])
    output_parser = epp.branch(total)
    return epp.chain(
        [epp.literal("{bg}"),
         epp.effect(lambda val, st: output_parser)],
        save_iterator=False)


def _make_name():
    """ Make a name parser. """
    output_parser = epp.chain(
        [epp.greedy(epp.everything()),
         epp.effect(lambda val, st: val.update({Capture.NAME: misc.normalize(st.parsed)}))],
        save_iterator=False)
    return epp.chain(
        [epp.literal("{name}"),
         epp.effect(lambda val, st: output_parser)],
        save_iterator=False)


def _make_pc(game):
    """ Make a PC name parser. """
    def specific_pc_parser(pc):
        """ Make a parser for a specific PC. """
        name = epp.literal(misc.normalize(pc.name))
        aliases = epp.multi(pc.aliases)
        eff = epp.effect(lambda val, st: val.update({Capture.PC: pc}))
        return epp.chain(
            [epp.branch([name, aliases], save_iterator=False),
             eff],
            save_iterator=False)
    def parser_generator():
        """ Generate a PC parser. """
        variants = map(specific_pc_parser, game.party.characters)
        catchall = epp.chain(
            [epp.greedy(epp.everything()),
             epp.effect(lambda val, st: val.update({Capture.PC: None}))],
            save_iterator=False)
        return epp.branch(chain(variants, [catchall]))
    return epp.chain(
        [epp.literal("{pc}"),
         epp.effect(lambda val, st: epp.lazy(parser_generator))],
        save_iterator=False)


def _make_species(game):
    """ Make a species parser. """
    def variant(species):
        """ Make a parser for the species. """
        fullname = epp.literal(misc.normalize(species.name))
        shortname = epp.literal(misc.normalize(species.shortname))
        eff = epp.effect(lambda val, st: val.update({Capture.SPECIES: species}))
        return epp.chain(
            [epp.branch([fullname, shortname], save_iterator=False),
             eff],
            save_iterator=False)
    catchall = epp.chain(
        [epp.greedy(epp.everything()),
         epp.effect(lambda val, st: val.update({Capture.SPECIES: None}))],
        save_iterator=False)
    total = chain(map(variant, game.data.species), [catchall])
    output_parser = epp.branch(total)
    return epp.chain(
        [epp.literal("{species}"),
         epp.effect(lambda val, st: output_parser)],
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
