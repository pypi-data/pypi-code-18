
"""
Determine height and width of current terminal.

Combines best methods mentioned in:
http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
"""

__all__ = ['get_terminal_size']


# Mimic the terminal_size struct the os, shutil, and posix modules return
# from C code
from collections import namedtuple
terminal_size = namedtuple('terminal_size', 'columns lines')


DEFAULT_ANSWER = terminal_size(lines=24, columns=80) # 1985 all over again

def from_os_module():
    # requires Python 3.3 or later
    import os
    return os.get_terminal_size(0)

def from_curses_module():
    # best fallback
    import curses
    w = curses.initscr()
    height, width = w.getmaxyx()
    return terminal_size(lines=height, columns=width)


def from_stty():
    # fallback request to shell
    # stty common on Linux and macOS
    import subprocess
    tup = subprocess.check_output(['stty', 'size']).decode().split()
    return terminal_size(lines=int(tup[0]), columns=int(tup[1]))


def get_terminal_size():
    """
    Mimic os.get_terminal_size() (minus the file descriptor paramter).
    Has several different mechanisms, used in turn. If nothing
    sticks, returns a default value.
    """
    methods = [from_os_module, from_curses_module, from_stty]
    for method in methods:
        try:
            return method()
        except Exception:
            pass
    return DEFAULT_ANSWER
