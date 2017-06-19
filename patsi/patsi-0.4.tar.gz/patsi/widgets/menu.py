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
from .widget import Widget
from .geometry import Point, Rect
from ._util import next_object
import curses


class Menu(Widget):
    class Item(object):
        def __init__(self, text, action=lambda: None, display_flags=0, auto_activate=False):
            self.text = text
            self.action = action
            self.display_flags = display_flags
            self.auto_activate = auto_activate

    def __init__(self, parent, window, items=[], width=16):
        self.width = width
        super(Menu, self).__init__(parent, window)
        self.items = items
        self.current = items[0] if items else None
        self.submenu = []

    def window_bounds_hint(self, parent_bounds):
        return Rect(
            top_left=Point(parent_bounds.right - self.width, parent_bounds.top),
            bottom_right=parent_bounds.bottom_right
        )

    def key_event(self, event):
        if event.key == curses.KEY_UP:
            self._switch_item(-1)
        elif event.key == curses.KEY_DOWN:
            self._switch_item(+1)
        elif event.key == curses.KEY_ENTER:
            self.activate()
        elif event.key == curses.KEY_BACKSPACE:
            if self.submenu:
                self.pop_submenu()
        elif event.key == curses.KEY_HOME:
            if not self.items:
                self._change_current(None)
            else:
                self._change_current(self.items[0])
        elif event.key == curses.KEY_END:
            if not self.items:
                self._change_current(None)
            else:
                self._change_current(self.items[-1])

    def text_event(self, event):
        if event.char == " ":
            self.activate()

    def _switch_item(self, delta):
        if not self.items:
            self._change_current(None)
        elif not self.current:
            self._change_current(self.items[0])
        else:
            self._change_current(next_object(self.items, self.current, delta))

    def _change_current(self, item):
        self.current = item

        if self.current is not None and self.current.auto_activate:
            self.current.action()

        self.refresh()

    def activate(self):
        if self.current:
            self.current.action()

    def _starting_y(self):
        return int(
            self.window_bounds().top +
            (self.window_bounds().height - len(self.items)) / 2
        )

    def render(self):
        y = self._starting_y()
        for item in self.items:
            if item is not self.current:
                mode = 0
            elif self.has_focus():
                mode = curses.A_REVERSE
            else:
                mode = curses.A_UNDERLINE
            self.window.addstr(y, 1, item.text, mode|item.display_flags)
            y += 1
        # TODO handle overflow

        self._draw_border()

    def focus_event(self, event):
        if event.focus and not self.current and self.items:
            self.current = self.items[0]
        super(Menu, self).focus_event(event)

    def push_submenu(self, items):
        self.submenu.append((self.items, self.current))
        self.items = items
        self.current = items[0] if items else None
        self.refresh()

    def pop_submenu(self):
        if not self.submenu:
            raise OverflowError("Underflow")
        cur_items = self.items
        self.items, self.current = self.submenu.pop()
        self.refresh()
        return cur_items

    def mouse_event(self, event):
        super(Menu, self).mouse_event(event)
        if event.buttons == curses.BUTTON1_CLICKED:
            index = event.pos.y - self._starting_y()
            if 0 <= index < len(self.items):
                self._change_current(self.items[index])
                self.activate()
                self.refresh()
            event.accept()
