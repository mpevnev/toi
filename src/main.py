#!/usr/bin/python
""" Main module. """


import mofloc


import toi.stage.startup as start


if __name__ == "__main__":
    flow = start.StartupFlow()
    mofloc.execute(flow, start.ENTRY_POINT)
