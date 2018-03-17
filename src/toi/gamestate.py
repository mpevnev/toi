"""
Game State module.

Provides GameState base class used to hold various game information: just
common control parsers and game data in its minimal configuration. The class is
supposed to be subclassed for concrete Flows.
"""


import toi.cat as cat
import toi.cat.common as common
from toi.parser import make_parser


class GameState():
    """ 
    A container for game information.
    """

    def __init__(self, data):
        self.data = data
        self.common_parsers = self.generate_common_parsers(data)

    def generate_common_parsers(self, data):
        """ Generate parsers common to all flows. """
        control = data.control[cat.COMMON]
        res = {}
        res[common.CMD_HELP] = make_parser(control[common.CMD_HELP], self)
        res[common.CMD_QUIT] = make_parser(control[common.CMD_QUIT], self)
        res[common.CMD_YES] = make_parser(control[common.CMD_YES], self)
        res[common.CMD_NO] = make_parser(control[common.CMD_NO], self)
        res[common.CMD_ABORT] = make_parser(control[common.CMD_ABORT], self)
        return res
