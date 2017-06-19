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
import curses
from ._util import next_object


class TabBar(Widget):
    def __init__(self, parent, window, items, current, formatter=str, separator="|"):
        super(TabBar, self).__init__(parent, window)
        self.items = items
        self.current = current
        self.formatter = formatter
        self.separator = separator
        self.signal_changed = lambda x: None
        self.render()

    def render(self):
        p = Point()
        self._draw_string(p, self.separator)
        p.x += len(self.separator)
        for item in self.items:
            if item is not self.current:
                mode = curses.A_NORMAL
            elif self.has_focus():
                mode = curses.A_REVERSE
            else:
                mode = curses.A_UNDERLINE
            text = self.formatter(item)
            self._draw_string(p, text, mode)
            p.x += len(text)
            self._draw_string(p, self.separator)
            p.x += len(self.separator)
        # TODO handle overflow

    def key_event(self, event):
        if event.key == curses.KEY_LEFT:
            self._switch_element(-1)
        elif event.key == curses.KEY_RIGHT:
            self._switch_element(+1)
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

    def _switch_element(self, delta):
        if not self.items:
            self._change_current(None)
        else:
            self._change_current(next_object(self.items, self.current, delta))

    def window_bounds_hint(self, parent_bounds):
        return Rect(
            top_left=parent_bounds.top_left,
            bottom_right=Point(
                parent_bounds.right,
                parent_bounds.top + 1,
            )
        )

    def _change_current(self, next):
        if next != self.current:
            self.current = next
            self.signal_changed(self.current)
            self.refresh()

    def mouse_event(self, event):
        super(TabBar, self).mouse_event(event)
        if event.buttons == curses.BUTTON1_CLICKED:
            x = len(self.separator)
            for item in self.items:
                length = len(self.formatter(item))
                if x < event.pos.x < x + length:
                    self._change_current(item)
                    break
                x += length
            event.accept()


class TabArea(Widget):
    def window_bounds_hint(self, parent_bounds):
        bounds = parent_bounds.copy()
        bounds.y1 = bounds.y1 + 1
        return bounds


class TabWidget(Widget):
    def __init__(self, parent, window, formatter=lambda x: "tab"):
        super(TabWidget, self).__init__(parent, window)

        self.current_tab = None
        self.container = TabArea(self)
        self.tabs = self.container.children

        self.bar = TabBar(self, None, self.tabs, None, formatter)
        self.bar.signal_changed = self._switch_current
        self.bar.items = self.tabs
        self.focus(self.bar)

    def close_current(self):
        if not self.current_tab:
            return

        index = self.tabs.index(self.current_tab)
        self.tabs.remove(self.current_tab)
        self.current_tab = None
        if self.tabs:
            if index == len(self.tabs):
                index -= 1
            self._switch_current(self.tabs[index])
        else:
            self.refresh()

    def create_tab(self, widget_class=Widget, *args, **kwargs):
        widget = self.create_tab_noadd(widget_class, *args, **kwargs)
        self.add_tab(widget)
        return widget

    def create_tab_noadd(self, widget_class=Widget, *args, **kwargs):
        return widget_class(None, self.container.window, *args, **kwargs)

    def add_tab(self, widget):
        widget.parent = self.container
        if widget not in self.tabs:
            self.tabs.append(widget)
        self._switch_current(widget)
        self.activate_tab()

    def _switch_current(self, tab):
        if tab != self.current_tab:

            old_tab = self.current_tab
            if old_tab:
                old_tab.active = False

            self.current_tab = tab
            self.bar.current = tab

            if tab:
                tab.active = True
                self.container.focus(tab)

            self.refresh()

    def on_activated(self, tab):
        pass

    def activate_tab(self):
        if self.current_tab:
            self.current_tab.active = True
            self.focus(self.container)
            self.on_activated(self.current_tab)
            self.current_tab.refresh()
