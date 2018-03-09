#!/usr/bin/python
""" Main module. """


import mofloc


import toi.stage.startup as start


def main():
    """ Main loop. """
    flow = start.StartupFlow()
    mofloc.execute(flow, start.ENTRY_POINT)

if __name__ == "__main__":
    main()
