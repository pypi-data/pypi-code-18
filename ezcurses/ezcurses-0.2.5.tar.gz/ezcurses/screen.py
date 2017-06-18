import curses
from functools import wraps


VALID_COLORS = {'black', 'red', 'green', 'yellow', 'blue', 'magenta',
                'cyan', 'white'}
KEY_MAP = {
    9: 'TAB',
    10: 'ENTER',
    27: 'ESCAPE',
    32: ' ',
    70: 'F1',
    258: 'DOWN',
    259: 'UP',
    260: 'LEFT',
    261: 'RIGHT',
    262: 'HOME',
    263: 'BACKSPACE',
    266: 'F2',
    267: 'F3',
    268: 'F4',
    269: 'F5',
    270: 'F6',
    271: 'F7',
    272: 'F8',
    273: 'F9',
    276: 'F12',
    330: 'DELETE',
    331: 'INSERT',
    336: 'SHIFT_DOWN',
    337: 'SHIFT_UP',
    338: 'PAGEDOWN',
    339: 'PAGEUP',
    360: 'END',
    393: 'SHIFT_LEFT',
    402: 'SHIFT_RIGHT',
    410: 'F1',
}


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
            self._area.addstr(int(pos[1]), int(pos[0]), msg,
                              curses.color_pair(ncol))
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
        return int(w), int(h)

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
        self._area.hline(int(pos[1]), int(pos[0]), c, int(n))

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
        self._area.vline(int(pos[1]), int(pos[0]), c, int(n))

    def change_color(self, pos=None, n=1, color=None):
        '''
        Change the color of all characters in this line.

        :param pos: the position to change, default (0, 0)
        :param n: the number of characters to the right to change, default 1
        :param color: the optional foreground or (fg, bg) colors
        '''
        pos = pos or (0, 0)
        ncol = self._add_colors(color)
        self._area.chgat(int(pos[1]), int(pos[0]), int(n),
                         curses.color_pair(ncol))

    @_echo
    def getstr(self, pos=None):
        '''
        Get an input string at a position, returned on pressing Enter.

        :param pos: the optional position, default (0, 0)
        :param echo: whether to echo the string while typing, default False
        :return: the string typed
        '''
        pos = pos or (0, 0)
        return self._area.getstr(int(pos[1]), int(pos[0])).decode('utf8')

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
        key = self._area.getch()
        return KEY_MAP.get(key, chr(key))

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

    def move_cursor(self, pos=None):
        '''
        Move the text cursor to the new position.

        :param pos: the new position (x, y) or default (0, 0)
        '''
        pos = pos or (0, 0)
        self._area.move(int(pos[1]), int(pos[0]))

    def get_menu_item(self, items, orig=None, force=False, color=None,
                      selected_color=None):
        '''
        Make a new menu in the screen or window.

        :param items: the list of (key char, item string) menu items. Use None
            as a key if you don't want a hotkey for that menu item.
        :param orig: optional origin, default (0, 0)
        :param force: force the user to make a choice, instead of returning None
            on ESCAPE.
        :param color: the foreground color of the menu item text, or (fg, bg),
            defaults to ('white', 'black') or white on black background
        :param selected_color: the foreground color of the selected menu item
            text, or (fg, bg), defaults to reverse of color
        '''
        menu = _Menu(items, color=color, selected_color=selected_color)
        if hasattr(self, '_screen'):
            menu.new_win(self._screen, orig=orig)
        else:
            menu.new_win(self, orig=orig)
        return menu.get_item(force=force)


class Window(Screen):

    def __init__(self, screen, orig=None, size=None):
        orig = orig or (0, 0)
        size = size or screen._max_size(window_orig=orig)
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newwin(int(size[1]), int(size[0]),
                                   int(orig[1]), int(orig[0]))

    def move_window(self, orig=None):
        '''
        Move the window to a new origin.

        :param orig: the new (x, y) or default (0, 0)
        '''
        orig = orig or (0, 0)
        self._area.mvwin(int(orig[1]), int(orig[0]))


class Pad(Screen):

    def __init__(self, screen, size=None):
        size = size or screen.max_size()
        self._screen = screen
        self._colors = screen._colors
        self._area = curses.newpad(size[1], int(size[0]))

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
        self._area.refresh(
            int(orig[1]), int(orig[0]),
            int(top_left[1]), int(top_left[0]),
            int(bottom_right[1]), int(bottom_right[0])
        )
        if clear:
            self._area.clear()


class _Menu:

    def __init__(self, msgs, color=None, selected_color=None):
        color = color or ('white', 'black')
        if isinstance(color, str):
            color = (color, 'black')
        if isinstance(selected_color, str):
            selected_color = (selected_color, 'white')
        self._color = color
        self._selected_color = selected_color or tuple(list(color)[::-1])
        self._msgs = msgs
        self.selected = 0
        self._size = (max(len(b) + 3 for _, b in msgs), len(msgs))
        self._choices = dict(msgs)

    def new_win(self, scr, orig=None):
        self._win = scr.new_win(orig=orig, size=self._size)
        self._scr = scr
        self._orig = orig or (0, 0)

    def draw(self):
        self._scr.refresh()
        for i, key_msg in enumerate(self._msgs):
            if self.selected == i:
                color = self._selected_color
            else:
                color = self._color
            key, msg = key_msg
            if key is None:
                self._win.write('   {}'.format(msg), pos=(0, i), color=color)
            else:
                self._win.write('{}) {}'.format(key, msg), pos=(0, i),
                                color=color)
        self._win.move_cursor((0, self.selected or 0))
        self._win.refresh()

    def get_item(self, force=False):
        while True:
            self.draw()
            key = self._scr.getkey()
            if key is not None and key in self._choices:
                return self._choices[key]
            if key == 'DOWN':
                self.selected += 1
                self.selected = self.selected % len(self._msgs)
            elif key == 'UP':
                self.selected -= 1
                self.selected = self.selected % len(self._msgs)
            elif key == 'ENTER':
                return self._msgs[self.selected][1]
            elif key == 'ESCAPE':
                if force:
                    continue
                return None


class Layout:
    '''
    Helps design a layout flow.
    '''

    def debug(self, msg, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        with open('debug.log', 'a') as f:
            f.write(msg + '\n')

    def __init__(self, area, border=True):
        self._area = area
        self.w, self.h = self._area.max_size()
        self.rows = []
        self._wins = []
        self.border = border

    def __getitem__(self, item):
        return self.rows[item]

    def __iter__(self):
        yield from self.rows

    def _calc_height(self, num):
        return int((num / 12) * self.h)

    def _calc_width(self, num):
        return int((num / 12) * self.w)

    def add_row(self, height, sizes=None):
        self.debug('new row: {!r}, {!r}', height, sizes)
        sizes = sizes or [12]
        new = LayoutRow(self, height, sizes)
        self.rows.append(new)
        return new

    def draw(self):
        self._area.refresh()
        self._wins = []
        ht = 0
        for row in self.rows:
            ht2 = self._calc_height(row.height)
            row.draw((0, ht), (self.w, ht2), border=self.border)
            ht += ht2


class LayoutRow(Layout):
    '''
    A row in the layout.
    '''

    def __init__(self, layout, height, sizes):
        self._layout = layout
        self.sizes = sizes
        self.height = height
        self.columns = []

    @property
    def w(self):
        return self._layout.w

    @property
    def h(self):
        return self._layout.h

    def __getitem__(self, item):
        return self.columns[item]

    def __iter__(self):
        yield from self.columns

    def draw(self, orig, size, border=True):
        self.columns = []
        w, h = size
        x, y = orig
        for size in self.sizes:
            col_size = self._calc_width(size)
            self.debug('new col: ({!r}, {!r}), ({!r}, {!r})',
                       x, y, col_size, h)
            col = self._layout._area.new_win(orig=(x, y), size=(col_size, h))
            if border:
                col.border()
            self.columns.append(col)
            col.refresh()
            x += col_size


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
