"""

Processor module.

Provides base Processor class for pieces of game logic.

"""

from collections import deque
import enum

import epp

import toi.cat as cat
import toi.cat.common as common


#--------- base classes ---------#


class Processor():
    """ A piece of game logic. """

    def __init__(self, prev=None):
        if prev is None:
            self.data = None
            self.control = None
            self.strings = None
            self.help = None
            self.io = None
            self.state = None
        else:
            self.data = prev.data
            self.control = prev.control
            self.strings = prev.strings
            self.help = prev.help
            self.io = prev.io
            self.state = prev.state
        self.commands = {}

    def run(self):
        """ Execute some game flow. """
        try:
            return self._run()
        except NextProcessor as exc:
            return exc.proc

    def command(self, string):
        """
        Execute a command.

        Return a tuple (command, command's return value) if some command was
        executed, or None if no command was executed.
        """
        matches = deque()
        for category in self.commands:
            for cmd in self.commands[category]:
                cmd = self.commands[category][cmd]
                args = cmd.match(string)
                if args is not None:
                    matches.append((cmd, args))
        if len(matches) > 1:
            self.io.say(self.strings[cat.S_COMMON][common.AMBIG_CMD])
            for m in matches:
                self.io.say("*", m[0].name)
            return None
        try:
            cmd, args = matches[0]
            return cmd.run(args)
        except IndexError:
            self.io.say(self.strings[cat.S_COMMON][common.WHAT])
            return None

    def make_command(self, method, category, name):
        """ Register a command. """
        parser = self.make_parser(category, name)
        if category not in self.commands:
            self.commands[category] = {}
        self.commands[category][name] = Command(name, method, parser)

    def make_parser(self, category, name):
        """
        Return a parser from control category 'category', represented in the
        control files by 'name'.
        """
        alters = deque()
        for alternative in self.control[category][name]:
            alters.append(self._make_parser_alternative(category, name, alternative))
        return epp.branch(alters)

    def _make_parser_alternative(self, category, name, string):
        """
        Return one of the alternative parsers for a given name and category.
        """
        word = epp.chain(
            [epp.many(epp.nonwhite_char(), 1),
             epp.effect(lambda val, st: val.append(_Literal(st.parsed)))])
        parser = epp.chain(
            [word,
             epp.effect(lambda val, st: val.to_parser(self))])
        output = epp.parse(_Group(), string, parser)
        if output is None:
            raise InvalidParser(category, name, string)
        return output[0]

    def _run(self):
        """ Execute some game flow. """
        raise NotImplementedError


class YesNo(enum.Enum):
    """ An enumeration for simple yes/no/abort questions. """
    NO = enum.auto()
    YES = enum.auto()
    ABORT = enum.auto()


class NextProcessor(Exception):
    """ An exception to be thrown when a processor exits. """

    def __init__(self, next_proc):
        super().__init__("Uncaught NextProcessor signal")
        self.proc = next_proc


class Command():
    """
    A unit of user interaction. A method 'Command' wraps should accept a dict
    with command arguments as a single argument.
    """

    def __init__(self, name, method, parser):
        self.name = name
        self.method = method
        self.parser = parser

    def match(self, string):
        """
        Return a dict with named captures if 'string' is a valid command
        invocation, or None otherwise.
        """
        return epp.parse({}, string, self.parser)

    def run(self, arg_dict):
        """ Run the command. """
        return self.method(arg_dict)


#--------- helper things ---------#


class InvalidParser(Exception):
    """
    This exception will be thrown if parser syntax used in control files is
    invalid.
    """

    def __init__(self, category, name, parser_source):
        s = f"Invalid command syntax for parser {category}/{name}: \"{parser_source}\""
        super().__init__(s)


#--------- private helper things ---------#

class _Piece():
    """ An abstract class for parsers construction. """

    def to_parser(self, processor):
        """ Transform the piece into a parser. """
        raise NotImplementedError

class _Literal(_Piece):
    """ A literal word. """

    def __init__(self, string):
        self.string = string

    def to_parser(self, processor):
        return epp.literal(self.string)

class _Optional(_Piece):
    """ An optional word or a group. """

    def __init__(self, group):
        self.group = group

    def to_parser(self, processor):
        return epp.maybe(self.group.to_parser(processor))

class _Group(_Piece):
    """ A group of words or other constructs. """

    def __init__(self):
        self.pieces = deque()

    def append(self, piece):
        """ Add a piece to the group. """
        self.pieces.append(piece)
        return self

    def to_parser(self, processor):
        pieces = list(map(lambda piece: piece.to_parser(processor), self.pieces))
        return epp.weave(pieces, epp.whitespace())
