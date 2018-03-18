"""
Statistics module.

Provides player character statistic types.
"""


import enum


class Stat(enum.Enum):
    """ Player character statistics. """
    STR = "str"
    DEX = "dex"
    INT = "int"
    SPI = "spi"
    CHA = "cha"
    LUC = "luc"
