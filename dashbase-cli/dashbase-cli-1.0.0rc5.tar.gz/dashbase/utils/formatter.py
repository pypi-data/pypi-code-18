from __future__ import unicode_literals

import os

import texttable


def get_tty_width():
    tty_size = os.popen('stty size 2> /dev/null', 'r').read().split()
    if len(tty_size) != 2:
        return 0
    _, width = tty_size
    return int(width)


class Table(texttable.Texttable):
    def __init__(self):
        texttable.Texttable.__init__(self, max_width=get_tty_width())
        self.set_chars(['-', '|', '+', '-'])
        self.set_deco(self.HEADER)
