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
        if colors is None:
            return 0
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

    def write(self, msg, pos=None, color=None):
        '''
        Write a message to the screen, window or pad at a position.

        :param msg: the message to write
        :param pos: the position to write the message in, default (0, 0)
        :param color: the optional foreground color or (foreground, background)
        '''
        pos = pos or (0, 0)
        ncol = self._add_colors(color)
        try:
            self._area.addstr(pos[1], pos[0], msg, curses.color_pair(ncol))
        except:
            pass

    def erase(self):
        '''
        Erase the screen, window or pad.
        '''
        self._area.erase()

    def refresh(self):
        '''
        Draw out the changes to the screen, window or pad.
        '''
        self._area.refresh()

    def clear(self):
        '''
        Clears the screen, window, or pad.
        '''
        self._area.clear()

    def _max_size(self, pad_orig=None, window_orig=None):
        w, h = self.max_size()
        if pad_orig is not None:
            w = w + pad_orig[0] - 1
            h = h + pad_orig[1] - 1
        elif window_orig is not None:
            w = w - window_orig[0] - 1
            h = h - window_orig[1] - 1
        else:
            raise ValueError('_max_size called without arguments')
        return w, h

    def max_size(self):
        '''
        The width and height of the screen

        :return: (width, height)
        '''
        h, w = self._area.getmaxyx()
        return w, h

    def new_pad(self, size=None):
        '''
        Create a new pad from the screen

        :param size: optional (width, height), default the max terminal
        :return: the new Pad instance
        '''
        return Pad(self, size=size)

    def new_win(self, orig=None, size=None):
        '''
        Create a new window from the screen.

        :param orig: the optional origin, default (0, 0) or top left
        :param size: the optional size, (width, height)
        :return: the new Window instance
        '''
        return Window(self, orig=orig, size=size)

    def hline(self, c, pos=None, n=None):
        '''
        Draw a horizontal line

        :param c: the character to use
        :param pos: the optional position to start at, default (0, 0)
        :param n: the optional length, default max width
        '''
        pos = pos or (0, 0)
        w, h = self.max_size()
        if n is None:
            n = w - pos[0]
        self._area.hline(pos[1], pos[0], c, n)

    def vline(self, c, pos=None, n=None):
        '''
        Draw a vertical line

        :param c: the character to use
        :param pos: the optional position to start at, default (0, 0)
        :param n: the optional length, default max height
        '''
        pos = pos or (0, 0)
        w, h = self.max_size()
        if n is None:
            n = h - pos[1]
        self._area.vline(pos[1], pos[0], c, n)

    def change_color(self, pos=None, n=1, color=None):
        '''
        Change the color of all characters in this line.

        :param pos: the position to change, default (0, 0)
        :param n: the number of characters to the right to change, default 1
        :param color: the optional foreground or (fg, bg) colors
        '''
        pos = pos or (0, 0)
        ncol = self._add_colors(color)
        self._area.chgat(pos[1], pos[0], n, curses.color_pair(ncol))

    @_echo
    def getstr(self, pos=None):
        '''
        Get an input string at a position, returned on pressing Enter.

        :param pos: the optional position, default (0, 0)
        :param echo: whether to echo the string while typing, default False
        :return: the string typed
        '''
        pos = pos or (0, 0)
        return self._area.getstr(pos[1], pos[0])

    @_echo
    def getch(self, **kwargs):
        '''
        Get an input character as a one-length string, one key press.

        :param echo: whether to echo the character while typing, default False
        :return: the character typed
        '''
        return self._area.getch()

    @_echo
    def getkey(self, **kwargs):
        '''
        Get an input character as an integer (chr/ord), one key press.

        :param echo: whether to echo the character while typing, default False
        :return: the integer value of the character typed
        '''
        return self._area.getkey()

    def background(self, c, color=None):
        '''
        Draw out a character across the window with an optional color.

        :param c: the character to fill the window with.
        :param color: the foreground or (fg, bg) colors
        '''
        ncol = self._add_colors(color)
        self._area.bkgd(c, curses.color_pair(ncol))

    def border(self, h=None, v=None):
        '''
        Draw out a border around a window, with configurable characters.

        :param h: the optional horizontal line character used on top/bottom
        :param v: the optional vertical line character used on left/right
        '''
        if any([h, v]):
            h = h or chr(0)
            v = v or chr(0)
            self._area.box(ord(v), ord(h))
        else:
            self._area.box()


class Window(Screen):

    def __init__(self, screen, orig=None, size=None):
        orig = orig or (0, 0)
        size = size or screen._max_size(window_orig=orig)
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newwin(size[1], size[0], orig[1], orig[0])


class Pad(Screen):

    def __init__(self, screen, size=None):
        size = size or screen.max_size()
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newpad(size[1], size[0])

    def refresh(self, orig=None, top_left=None, bottom_right=None, clear=False):
        '''
        Draw out the changes.

        :param orig: the optional origin of where to start the top left in the
            pad, default (0, 0) or the very top left of the full pad
        :param top_left: where to start the pad update, default (0, 0)
        :param bottom_right: where to end the pad update,
            default (width, height)
        :param clear: clear for the next refresh, default False
        '''
        orig = orig or (0, 0)
        top_left = top_left or (0, 0)
        bottom_right = bottom_right or self._screen._max_size(pad_orig=orig)
        self._area.refresh(orig[1], orig[0], top_left[1], top_left[0],
                           bottom_right[1], bottom_right[0])
        if clear:
            self._area.clear()


class Cursed:
    '''
    Cursed is a context manager that handles the setup and resetting of the
    terminal for curses programming.

    Just wrap your code with::

        with Cursed() as scr:
            ...

    And either use the ``scr`` variable, or create windows or pads from it with
    ``scr.new_win`` or ``scr.new_pad``.
    '''

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


def curse(func):

    @wraps(func)
    def decorator(*args, **kwargs):
        with Cursed() as scr:
            return func(scr, *args, **kwargs)
    return decorator
