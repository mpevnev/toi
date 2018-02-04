#!/usr/bin/python

""" Main module. """

import toi.stage.startup as start

def main():
    """ Main loop. """
    proc = start.Processor()
    while proc is not None:
        proc = proc.run()

if __name__ == "__main__":
    main()
