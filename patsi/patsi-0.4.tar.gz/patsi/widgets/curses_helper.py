#
# Copyright (C) 2016-2017 Mattia Basaglia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import curses
from contextlib import contextmanager


@contextmanager
def curses_context():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.nonl()
    stdscr.keypad(1)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK,     -1)
    curses.init_pair(2, curses.COLOR_RED,       -1)
    curses.init_pair(3, curses.COLOR_GREEN,     -1)
    curses.init_pair(4, curses.COLOR_YELLOW,    -1)
    curses.init_pair(5, curses.COLOR_BLUE,      -1)
    curses.init_pair(6, curses.COLOR_MAGENTA,   -1)
    curses.init_pair(7, curses.COLOR_CYAN,      -1)
    curses.init_pair(8, curses.COLOR_WHITE,     -1)

    try:
        yield stdscr
    finally:
        stdscr.keypad(0)
        curses.nl()
        curses.nocbreak()
        curses.echo()
        curses.endwin()


def color_to_curses(color):
    if color is None:
        return curses.A_NORMAL | curses.color_pair(0)
    flags = curses.color_pair((color.index & 7) + 1)
    if color.index & 8:
        flags |= curses.A_BOLD
    return flags
