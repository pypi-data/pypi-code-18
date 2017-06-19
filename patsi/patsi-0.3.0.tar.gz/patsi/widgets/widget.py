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
import six
import curses
import curses.ascii
from patsi.widgets.geometry import Point, Rect


class Event(object):
    TYPE_TEXT       = 1
    TYPE_KEY        = 2
    TYPE_RESIZE     = 3
    TYPE_MOUSE      = 4
    TYPE_FOCUS      = 5

    def __init__(self, type, **kwargs):
        self.type = type
        self.propagate = True
        for attr, val in six.iteritems(kwargs):
            setattr(self, attr, val)

    def accept(self):
        self.propagate = False

    @staticmethod
    def text_event(char):
        return Event(Event.TYPE_TEXT, char=char)

    @staticmethod
    def key_event(key):
        return Event(Event.TYPE_KEY, key=key)

    @staticmethod
    def resize_event(bounds):
        return Event(Event.TYPE_RESIZE, bounds=bounds)

    @staticmethod
    def mouse_event(pos, buttons):
        return Event(Event.TYPE_MOUSE, pos=pos, buttons=buttons)

    @staticmethod
    def focus_event(focus):
        return Event(Event.TYPE_FOCUS, focus=focus)


class Widget(object):
    def __init__(self, parent, window=None):
        self.parent = parent
        self.children = []
        self.focus_child = None
        self.active = True
        self.window = window

        if parent is not None:
            bounds = self.window_bounds_hint(parent.window_bounds())
            if window is None:
                self.window = parent.window.subwin(bounds.height, bounds.width, bounds.y, bounds.x)
            else:
                self.adjust_window_size(bounds)
            parent.children.append(self)
        elif window is None:
            self.window = curses.newwin(24, 80)

    def focus(self, *args):
        if not self.active:
            return

        if len(args) == 0 or args[0] is self:
            if self.parent:
                self.parent.focus(self)
            return

        if self.focus_child == args[0]:
            return

        if self.focus_child:
            self.focus_child.event(Event.focus_event(False))

        self.focus_child = args[0]

        if self.focus_child:
            self.focus_child.event(Event.focus_event(True))

    def has_focus(self):
        return self.active and (not self.parent or self.parent.focus_child == self)

    def window_bounds(self):
        return Rect(
            top_left=Point(*self.window.getbegyx(), reversed=True),
            bottom_right=Point(*self.window.getmaxyx(), reversed=True)
        )

    def window_bounds_hint(self, parent_bounds):
        return parent_bounds

    def loop(self):
        while self.active:
            self.refresh()
            self.get_input()

    def deactivate(self):
        self.active = False

    def get_input(self):
        ch = self.window.getch()
        event = None

        if ch == curses.KEY_RESIZE:
            event = Event.resize_event(self.window_bounds())
        elif ch == curses.KEY_MOUSE:
            try:
                id, x, y, z, bstate = curses.getmouse()
                event = Event.mouse_event(Point(x, y), bstate)
            except curses.error:
                pass
        elif curses.ascii.isprint(ch):
            event = Event.text_event(chr(ch))
        else:
            event = Event.key_event(ch)

        if event is not None:
            self.event(event)

    def event(self, event):
        if event.type == Event.TYPE_RESIZE:
            self.resize_event(event)
            if event.propagate:
                bounds = self.window_bounds()
                for child in self.children:
                    old_bounds = child.window_bounds()
                    new_bounds = child.window_bounds_hint(bounds)
                    if old_bounds != new_bounds:
                        child.event(Event.resize_event(new_bounds))
            return

        if not self.active:
            return

        if event.type == Event.TYPE_TEXT:
            self.text_event(event)
            if self.focus_child and event.propagate:
                self.focus_child.event(event)
        elif event.type == Event.TYPE_KEY:
            self.key_event(event)
            if self.focus_child and event.propagate:
                self.focus_child.event(event)
        elif event.type == Event.TYPE_MOUSE:
            self.mouse_event(event)
            if not event.propagate:
                return
            for child in self.children:
                if child.active and child.window_bounds().contains(event.pos):
                    if self.event_change_focus_child(child):
                        child_bounds = child.window_bounds()
                        relative = event.pos - child_bounds.pos
                        child_event = Event.mouse_event(relative, event.buttons)
                        child.event(child_event)
                        if not child_event.propagate:
                            return
        elif event.type == Event.TYPE_FOCUS:
            self.focus_event(event)

    def event_change_focus_child(self, new):
        self.focus_child = new
        return True

    def text_event(self, event):
        pass

    def key_event(self, event):
        pass

    def resize_event(self, event):
        self.adjust_window_size(event.bounds)

    def mouse_event(self, event):
        self.focus()

    def adjust_window_size(self, bounds):
        if self.window_bounds() != bounds:
            self.window.mvwin(bounds.y, bounds.x)
            self.window.resize(bounds.height, bounds.width)

    def refresh(self):
        self.window.clear()
        self.render()
        self.window.refresh()
        for child in self.children:
            if child.active:
                child.refresh()

    def render(self):
        pass

    def focus_event(self, event):
        if event.focus:
            self.refresh()

    def _draw_border(self):
        self.window.border("|", "|", "-", "-", "+", "+", "+", "+")

    def _draw_string(self, pos, text, *args):
        self.window.addstr(pos.y, pos.x, text, *args)
