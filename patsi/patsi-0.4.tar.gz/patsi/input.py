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
import sys
import tty
import termios
import contextlib


class RawInput(object):
    def __init__(self, read_ansi=True, raise_specials=True, non_blocking=True):
        self.file = sys.stdin
        self.fileno = self.file.fileno()
        self.attrs = None
        self.when = termios.TCSAFLUSH
        self.read_ansi = True
        self.raise_specials = True
        self.non_blocking = non_blocking

    def get(self):
        ch = self.file.read(1)

        if ch:
            code = ord(ch)
            if  code == 3 and self.raise_specials:
                raise KeyboardInterrupt()
            if code == 4 and self.raise_specials:
                raise EOFError()
            if code == 0x1b and self.read_ansi:
                with self.nonblocking():
                    ch += self.file.readline()
        return ch

    def getline(self):
        line = self.file.readline()
        if self.raise_specials:
            if '\3' in line:
                raise KeyboardInterrupt()
            if '\4' in line:
                raise EOFError()
        return line

    def __iter__(self):
        while True:
            yield self.get()

    def __enter__(self):
        if self.attrs is None:
            self.attrs = termios.tcgetattr(self.fileno)
            tty.setraw(self.fileno, self.when)
            if self.non_blocking:
                self._set_non_blocking(termios.tcgetattr(self.fileno))
        return self

    def __exit__(self, *a, **k):
        if self.attrs:
            termios.tcsetattr(self.fileno, self.when, self.attrs)

    @contextlib.contextmanager
    def nonblocking(self):
        if self.non_blocking:
            yield
            return

        mode = termios.tcgetattr(self.fileno)
        try:
            self._set_non_blocking(mode)
            yield
        finally:
            self._set_blocking(mode)

    def _set_non_blocking(self, mode):
        mode[tty.CC][termios.VMIN] = 0
        termios.tcsetattr(sys.stdin, self.when, mode)

    def _set_blocking(self, mode):
        mode[tty.CC][termios.VMIN] = 1
        termios.tcsetattr(sys.stdin, self.when, mode)
