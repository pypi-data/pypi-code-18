from __future__ import print_function
import sys

verbosity = 1

class Colors(object):
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[36m'
    RED= '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    RED_BG = '\033[41m'
    GREEN_BG = '\033[42m'
    YELLOW_BG = '\033[43m'
    BLUE_BG = '\033[44m'
    MAGENTA_BG = '\033[45m'


def eprint(to_print):
    """Print to stderr, regardless on verbose status"""
    print(
        "{0}{1}{2}".format(Colors.RED, to_print, Colors.ENDC), file=sys.stderr
    )

def vprint(needed_verbosity, color, to_print):
    """
    Print to stdout if verbosity is enough to do so.
    """
    if verbosity >= needed_verbosity:
        if color is not None:
            print("{0}{1}{2}".format(color, to_print, Colors.ENDC))
        else:
            print(to_print)
