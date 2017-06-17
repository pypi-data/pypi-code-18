import curses
from functools import wraps


VALID_COLORS = {'black', 'red', 'green', 'yellow', 'blue', 'magenta',
                'cyan', 'white'}


def _echo(func):

    @wraps(func)
    def deco(*args, echo=False, **kwargs):
        if echo:
            curses.echo()
        result = func(*args, **kwargs)
        if echo:
            curses.noecho()
        return result

    return deco


class Screen:

    def __init__(self, stdscr):
        self._area = stdscr
        self._colors = {}

    def _translate_color(self, color):
        if color not in VALID_COLORS:
            raise ValueError('color must be one of {!r}'.format(VALID_COLORS))
        attr = 'COLOR_{}'.format(color.upper())
        return getattr(curses, attr)

    def _add_colors(self, colors):
        if isinstance(colors, str):
            colors = (colors, 'black')
        colors = (
            self._translate_color(colors[0]),
            self._translate_color(colors[1])
        )
        if colors in self._colors:
            return self._colors[colors]
        n = len(self._colors) + 1
        curses.init_pair(n, *colors)
        self._colors[colors] = n
        return n

    def write(self, msg, pos, color=None):
        if color:
            ncol = self._add_colors(color)
        else:
            ncol = 0
        try:
            self._area.addstr(pos[1], pos[0], msg, curses.color_pair(ncol))
        except:
            pass

    def draw(self):
        self._area.refresh()

    def _max_size(self, pad_orig=None, window_orig=None):
        w, h = self.max_size()
        if pad_orig is not None:
            w = w + pad_orig[0] - 1
            h = h + pad_orig[1] - 1
            return w, h
        elif window_orig is not None:
            w = w - window_orig[0] - 1
            h = h - window_orig[1] - 1
        else:
            raise ValueError('_max_size called without arguments')

    def max_size(self):
        h, w = self._area.getmaxyx()
        return w, h

    def new_pad(self, size=None):
        return Pad(self, size=size)

    def new_win(self, orig=None, size=None):
        return Window(self, orig=orig, size=size)

    def hline(self, c, pos=None, n=None):
        pos = pos or (0, 0)
        w, h = self.max_size()
        if n is None:
            n = w - pos[0]
        self._area.hline(pos[1], pos[0], c, n)

    def vline(self, c, pos=None, n=None):
        pos = pos or (0, 0)
        w, h = self.max_size()
        if n is None:
            n = h - pos[1]
        self._area.vline(pos[1], pos[0], c, n)

    @_echo
    def getstr(self, *args):
        if len(args) == 0:
            pos = (0, 0)
        elif len(args) == 1:
            pos = args[0]
        else:
            pos = args[:2]
        return self._area.getstr(pos[1], pos[0])

    @_echo
    def getch(self, **kwargs):
        return self._area.getch()

    @_echo
    def getkey(self, **kwargs):
        return self._area.getkey()


class Window(Screen):

    def __init__(self, screen, orig=None, size=None):
        orig = orig or (0, 0)
        size = size or screen.max_size(window_orig=orig)
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newwin(size[1], size[0], orig[1], orig[0])


class Pad(Screen):

    def __init__(self, screen, size=None):
        size = size or screen.max_size()
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newpad(size[1], size[0])

    def draw(self, orig=None, top_left=None, bottom_right=None):
        orig = orig or (0, 0)
        top_left = top_left or (0, 0)
        bottom_right = bottom_right or self._screen._max_size(pad_orig=orig)
        self._area.refresh(orig[1], orig[0], top_left[1], top_left[0],
                           bottom_right[1], bottom_right[0])


class ezscreen:

    def __init__(self, noecho=True, cbreak=True, keypad=True):
        self.stdscr = curses.initscr()
        curses.start_color()
        if noecho:
            curses.noecho()
        if cbreak:
            curses.cbreak()
        self.stdscr.keypad(keypad)
        self.stdscr.clear()

    def __enter__(self):
        return Screen(self.stdscr)

    def __exit__(self, *args):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
