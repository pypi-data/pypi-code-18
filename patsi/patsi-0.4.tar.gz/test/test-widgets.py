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
from mock import patch
import test_common

from patsi.document import color, palette
from patsi import widgets
from patsi.widgets import geometry as geo
from patsi.widgets import _util as util


class TestPoint(test_common.TestCase):
    def assert_point(self, point, x, y):
        self.assertEqual(point.x, x)
        self.assertEqual(point.y, y)

    def test_ctor(self):
        self.assert_point(geo.Point(), 0, 0)
        self.assert_point(geo.Point(1, 2), 1, 2)
        self.assert_point(geo.Point(1, 2, reversed=True), 2, 1)
        self.assert_point(geo.Point((1, 2)), 1, 2)
        self.assert_point(geo.Point(x=1, y=2), 1, 2)

    def test_add(self):
        self.assert_point(geo.Point(1, 2) + geo.Point(30, 40), 31, 42)

        point = geo.Point(1, 2)
        point += geo.Point(30, 40)
        self.assert_point(point, 31, 42)

        self.assert_point(geo.Point(34, 43) - geo.Point(3, 1), 31, 42)

        point = geo.Point(34, 43)
        point -= geo.Point(3, 1)
        self.assert_point(point, 31, 42)

    def test_cmp(self):
        self.assertTrue(geo.Point(1, 2) == geo.Point(1, 2))
        self.assertFalse(geo.Point(1, 2) == geo.Point(1, 3))
        self.assertFalse(geo.Point(3, 2) == geo.Point(1, 2))

        self.assertFalse(geo.Point(1, 2) != geo.Point(1, 2))
        self.assertTrue(geo.Point(1, 2) != geo.Point(1, 3))
        self.assertTrue(geo.Point(3, 2) != geo.Point(1, 2))

    def test_interpolate(self):
        self.assert_point(geo.Point(4, 5).interpolate(geo.Point(2, 3)), 3, 4)
        self.assert_point(geo.Point(4, 5).interpolate(geo.Point(2, 3), 0), 4, 5)
        self.assert_point(geo.Point(4, 5).interpolate(geo.Point(2, 3), 1), 2, 3)

    def test_elements(self):
        point = geo.Point(4, 5)
        self.assertEqual(point[0], point.x)
        self.assertEqual(point["x"], point.x)
        self.assertEqual(point[1], point.y)
        self.assertEqual(point["y"], point.y)
        self.assertRaises(KeyError, lambda: point[2])
        self.assertRaises(KeyError, lambda: point["z"])

        x, y = point
        self.assert_point(point, x, y)
        self.assertEqual(tuple(point), (x, y))

    def test_repr(self):
        point = geo.Point(4, 5)
        self.assertEqual(str(point), str(tuple(point)))


class TestRect(test_common.TestCase):
    def assert_rect(self, rect, x1, y1, x2, y2):
        self.assertEqual(rect.top_left, geo.Point(x1, y1))
        self.assertEqual(rect.bottom_right, geo.Point(x2, y2))

    def test_ctor(self):
        tl = geo.Point(1, 2)
        br = geo.Point(11, 22)
        sz = geo.Point(10, 20)
        self.assert_rect(geo.Rect(pos=tl, size=sz), 1, 2, 11, 22)
        self.assert_rect(geo.Rect(top_left=tl, bottom_right=br), 1, 2, 11, 22)
        self.assert_rect(
            geo.Rect(x=tl.x, y=tl.y, width=sz.x, height=sz.y),
            1, 2, 11, 22
        )
        self.assert_rect(
            geo.Rect(x1=tl.x, y1=tl.y, x2=br.x, y2=br.y),
            1, 2, 11, 22
        )
        self.assert_rect(
            geo.Rect(top=tl.x, left=tl.y, bottom=br.x, right=br.y),
            1, 2, 11, 22
        )
        self.assert_rect(geo.Rect(), 0, 0, 0, 0)

    def test_contains(self):
        rect = geo.Rect(x1=10, y1=10, x2=20, y2=20)
        pin = geo.Point(12, 13)
        pout = geo.Point(14, 2)
        pbound = geo.Point(14, 10)

        self.assertTrue(rect.contains(pin))
        self.assertFalse(rect.contains(pout))
        self.assertTrue(rect.contains(pbound))

        self.assertTrue(rect.contains(pin, False))
        self.assertFalse(rect.contains(pout, False))
        self.assertFalse(rect.contains(pbound, False))

    def test_property_getters(self):
        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        self.assertEqual(rect.top_left, geo.Point(1, 2))
        self.assertEqual(rect.bottom_right, geo.Point(11, 32))
        self.assertEqual(rect.top_right, geo.Point(11, 2))
        self.assertEqual(rect.bottom_left, geo.Point(1, 32))
        self.assertEqual(rect.center, geo.Point(6, 17))

        self.assertEqual(rect.top, 2)
        self.assertEqual(rect.left, 1)
        self.assertEqual(rect.bottom, 32)
        self.assertEqual(rect.right, 11)

        self.assertEqual(rect.x1, 1)
        self.assertEqual(rect.y1, 2)
        self.assertEqual(rect.x2, 11)
        self.assertEqual(rect.y2, 32)

        self.assertEqual(rect.x, 1)
        self.assertEqual(rect.y, 2)
        self.assertEqual(rect.width, 10)
        self.assertEqual(rect.height, 30)

        self.assertEqual(rect.pos, geo.Point(1, 2))
        self.assertEqual(rect.size, geo.Point(10, 30))

    def test_property_setters(self):
        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.top_left = geo.Point(10, 20)
        self.assert_rect(rect, 10, 20, 11, 32)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.bottom_right = geo.Point(30, 40)
        self.assert_rect(rect, 1, 2, 30, 40)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.top_right = geo.Point(10, 20)
        self.assert_rect(rect, 1, 20, 10, 32)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.bottom_left = geo.Point(40, 20)
        self.assert_rect(rect, 40, 2, 11, 20)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.left = 4
        rect.top = 5
        rect.right = 6
        rect.bottom = 7
        self.assert_rect(rect, 4, 5, 6, 7)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.x = 101
        rect.y = 102
        self.assert_rect(rect, 101, 102, 111, 132)


        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.x1 = 101
        rect.y1 = 102
        self.assert_rect(rect, 101, 102, 11, 32)
        rect.x2 = 201
        rect.y2 = 202
        self.assert_rect(rect, 101, 102, 201, 202)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.pos = geo.Point(101, 102)
        self.assert_rect(rect, 101, 102, 111, 132)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.width = 100
        rect.height = 200
        self.assert_rect(rect, 1, 2, 101, 202)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.size = geo.Point(100, 200)
        self.assert_rect(rect, 1, 2, 101, 202)

        rect = geo.Rect(x1=1, y1=2, x2=11, y2=32)
        rect.center = geo.Point(0, 0)
        self.assert_rect(rect, -5, -15, 5, 15)

    def test_comparison(self):
        self.assertTrue(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) ==
            geo.Rect(x1=10, y1=20, x2=30, y2=40)
        )
        self.assertFalse(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) ==
            geo.Rect(x1=15, y1=20, x2=30, y2=40)
        )
        self.assertFalse(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) ==
            geo.Rect(x1=10, y1=25, x2=30, y2=40)
        )
        self.assertFalse(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) ==
            geo.Rect(x1=10, y1=20, x2=35, y2=40)
        )
        self.assertFalse(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) ==
            geo.Rect(x1=10, y1=20, x2=30, y2=45)
        )

        self.assertFalse(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) !=
            geo.Rect(x1=10, y1=20, x2=30, y2=40)
        )
        self.assertTrue(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) !=
            geo.Rect(x1=15, y1=20, x2=30, y2=40)
        )
        self.assertTrue(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) !=
            geo.Rect(x1=10, y1=25, x2=30, y2=40)
        )
        self.assertTrue(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) !=
            geo.Rect(x1=10, y1=20, x2=35, y2=40)
        )
        self.assertTrue(
            geo.Rect(x1=10, y1=20, x2=30, y2=40) !=
            geo.Rect(x1=10, y1=20, x2=30, y2=45)
        )

    def test_copy(self):
        r1 = geo.Rect(x1=10, y1=20, x2=30, y2=40)
        r2 = r1.copy()
        self.assertIsNot(r1, r2)
        r2.x1 = 100
        r2.y1 = 200
        r2.x2 = 300
        r2.y2 = 400
        self.assert_rect(r1, 10, 20, 30, 40)
        self.assert_rect(r2, 100, 200, 300, 400)

    def test_repr(self):
        rect = geo.Rect(x=10, y=20, width=30, height=40)
        self.assertEqual(str(rect), "Rect(30x40+10+20)")


class TestUtil(test_common.TestCase):
    def test_next_object(self):
        arr = [0, 1, 2, 3, 4]
        curr = 2
        self.assertEqual(4, util.next_object(arr, curr, -3))
        self.assertEqual(0, util.next_object(arr, curr, -2))
        self.assertEqual(1, util.next_object(arr, curr, -1))
        self.assertEqual(2, util.next_object(arr, curr, 0))
        self.assertEqual(3, util.next_object(arr, curr, 1))
        self.assertEqual(4, util.next_object(arr, curr, 2))
        self.assertEqual(0, util.next_object(arr, curr, 3))

        curr = None
        self.assertEqual(2, util.next_object(arr, curr, -3))
        self.assertEqual(3, util.next_object(arr, curr, -2))
        self.assertEqual(4, util.next_object(arr, curr, -1))
        self.assertEqual(0, util.next_object(arr, curr, 0))
        self.assertEqual(0, util.next_object(arr, curr, 1))
        self.assertEqual(1, util.next_object(arr, curr, 2))
        self.assertEqual(2, util.next_object(arr, curr, 3))

        self.assertEqual(curr, util.next_object([], curr, 3))

    @patch("curses.color_pair", side_effect=lambda x: 256 << (x-1) if x else 0)
    def test_color_to_curses(self, color_pair):
        color_conv = widgets.curses_helper.color_to_curses

        self.assertEqual(
            curses.A_NORMAL | curses.color_pair(0),
            color_conv(None)
        )

        self.assertEqual(
            curses.A_NORMAL | curses.color_pair(2),
            color_conv(color.IndexedColor(1, palette.colors16))
        )

        self.assertEqual(
            curses.A_BOLD | curses.color_pair(2),
            color_conv(color.IndexedColor(8|1, palette.colors16))
        )

    def test_curses_context(self):
        self.assertRaises(curses.error, lambda: curses.color_pair(1))
        with widgets.curses_helper.curses_context():
            self.assertFalse(curses.isendwin())
        self.assertTrue(curses.isendwin())


class MockCursesWindow(object):
    def __init__(self, nlines, ncols, begin_y=0, begin_x=0):
        self.rect = geo.Rect(x=begin_x, y=begin_y, width=ncols, height=nlines)
        self.strings = {}
        self.input_queue = []
        self.refreshed = False
        self.resized = False

    def subwin(self, nlines, ncols, begin_y, begin_x):
        return MockCursesWindow(nlines, ncols, begin_y, begin_x)

    def addstr(self, y, x, text, flags=0):
        self.strings[(x, y)] = (text, flags)

    def border(self, *args):
        pass

    def getbegyx(self):
        return (self.rect.top, self.rect.left)

    def getmaxyx(self):
        return (self.rect.bottom, self.rect.right)

    def getch(self):
        return self.input_queue.pop(0)

    def mvwin(self, new_y, new_x):
        self.rect.top_left = geo.Point(new_x, new_y)

    def resize(self, nlines, ncols):
        self.rect.size = geo.Point(ncols, nlines)
        self.resized = True

    def clear(self):
        self.strings.clear()
        self.refreshed = False

    def refresh(self):
        self.refreshed = True


class TestEvent(test_common.TestCase):
    def test_ctor(self):
        ev = widgets.Event(123, foo="bar")
        self.assertEqual(ev.type, 123)
        self.assertTrue(hasattr(ev, "foo"))
        self.assertEqual(ev.foo, "bar")
        self.assertTrue(ev.propagate)

    def test_accept(self):
        ev = widgets.Event(123)
        ev.accept()
        self.assertFalse(ev.propagate)

    def test_static(self):
        ev = widgets.Event.text_event("x")
        self.assertEqual(ev.type, widgets.Event.TYPE_TEXT)
        self.assertEqual(ev.char, "x")

        ev = widgets.Event.key_event(123)
        self.assertEqual(ev.type, widgets.Event.TYPE_KEY)
        self.assertEqual(ev.key, 123)

        ev = widgets.Event.resize_event(geo.Rect())
        self.assertEqual(ev.type, widgets.Event.TYPE_RESIZE)
        self.assertEqual(ev.bounds, geo.Rect())

        ev = widgets.Event.mouse_event(geo.Point(), 0)
        self.assertEqual(ev.type, widgets.Event.TYPE_MOUSE)
        self.assertEqual(ev.pos, geo.Point())
        self.assertEqual(ev.buttons, 0)

        ev = widgets.Event.focus_event(True)
        self.assertEqual(ev.type, widgets.Event.TYPE_FOCUS)
        self.assertEqual(ev.focus, True)


class TestWidget(test_common.TestCase):
    @patch("curses.newwin", new=lambda *args: MockCursesWindow(*args))
    def windows(self):
        parent = widgets.Widget(None)
        child = widgets.Widget(parent)
        return parent, child

    @contextmanager
    def no_event(self, widget, type=None):
        old = widget.event

        def noevent(event):
            if type is None or type == event.type:
                raise Exception("Event should not have been called")
            return old(event)

        widget.event = noevent
        try:
            yield
        finally:
            widget.event = old

    @contextmanager
    def must_event(self, widget, type, count=1):
        old = widget.event
        events = []

        def noevent(event):
            if type == event.type:
                events.append(event)
            return old(event)

        widget.event = noevent
        try:
            yield
        finally:
            widget.event = old
            self.assertEqual(len(events), count)

    @patch("curses.newwin", new=lambda *args: MockCursesWindow(*args))
    def test_ctor(self):
        window = MockCursesWindow(640, 480, 1, 2)
        wid = widgets.Widget(None, window)
        self.assertIsNone(wid.parent)
        self.assertEqual(wid.children, [])
        self.assertIsNone(wid.focus_child)
        self.assertTrue(wid.active)
        self.assertIs(wid.window, window)

        wid0 = widgets.Widget(None)
        self.assertIsNone(wid0.parent)
        self.assertEqual(wid0.children, [])
        self.assertIsNone(wid0.focus_child)
        self.assertTrue(wid0.active)
        self.assertIsInstance(wid0.window, MockCursesWindow)

        wid1 = widgets.Widget(wid)
        self.assertIs(wid1.parent, wid)
        self.assertIn(wid1, wid.children)
        self.assertEqual(wid1.children, [])
        self.assertIsNone(wid1.focus_child)
        self.assertTrue(wid1.active)
        self.assertIsInstance(wid1.window, MockCursesWindow)
        self.assertIsNot(wid1.window, wid.window)
        self.assertEqual(wid1.window.rect, wid.window.rect)

        window2 = MockCursesWindow(1, 2, 3, 4)
        wid2 = widgets.Widget(wid, window2)
        self.assertIs(wid2.parent, wid)
        self.assertIn(wid2, wid.children)
        self.assertEqual(wid2.children, [])
        self.assertIsNone(wid2.focus_child)
        self.assertTrue(wid2.active)
        self.assertIsInstance(wid2.window, MockCursesWindow)
        self.assertIs(wid2.window, window2)
        self.assertEqual(wid2.window.rect, wid.window.rect)

    def test_has_focus(self):
        parent, child = self.windows()

        self.assertTrue(parent.has_focus())
        parent.active = False
        self.assertFalse(parent.has_focus())
        parent.active = True

        self.assertFalse(child.has_focus())
        parent.focus(child)
        self.assertTrue(child.has_focus())
        child.active = False
        self.assertFalse(child.has_focus())
        child.active = True
        parent.focus(None)
        self.assertFalse(child.has_focus())

    def test_focus(self):
        parent, child = self.windows()

        parent.active = False
        parent.focus(child)
        self.assertFalse(child.has_focus())
        parent.active = True

        child.focus()
        self.assertTrue(child.has_focus())
        parent.focus(None)

        child.focus()
        with self.no_event(child):
            child.focus()
        parent.focus(None)

        sibling = widgets.Widget(parent)
        child.focus()
        self.assertTrue(child.has_focus())
        self.assertFalse(sibling.has_focus())
        with self.must_event(child, widgets.Event.TYPE_FOCUS):
            sibling.focus()
            self.assertTrue(sibling.has_focus())
            self.assertFalse(child.has_focus())
        parent.focus(None)

        parent.focus()

    def test_deactivate(self):
        parent, child = self.windows()
        self.assertTrue(parent.active)
        parent.deactivate()
        self.assertFalse(parent.active)

    @patch("curses.getmouse", new=lambda: (0, 1, 2, 0, 123))
    def test_get_input(self):
        parent, child = self.windows()
        parent.window.input_queue = [
            curses.KEY_RESIZE,
            curses.KEY_MOUSE,
            ord(" "),
            curses.KEY_HOME,
            curses.KEY_MOUSE,
        ]

        def event_replace(event):
            parent._last_event = event
        parent.event = event_replace

        parent.get_input()
        self.assertEqual(parent._last_event.type, widgets.Event.TYPE_RESIZE)
        self.assertEqual(parent._last_event.bounds, parent.window_bounds())

        parent.get_input()
        self.assertEqual(parent._last_event.type, widgets.Event.TYPE_MOUSE)
        self.assertEqual(parent._last_event.pos, geo.Point(1, 2))
        self.assertEqual(parent._last_event.buttons, 123)

        parent.get_input()
        self.assertEqual(parent._last_event.type, widgets.Event.TYPE_TEXT)
        self.assertEqual(parent._last_event.char, " ")

        parent.get_input()
        self.assertEqual(parent._last_event.type, widgets.Event.TYPE_KEY)
        self.assertEqual(parent._last_event.key, curses.KEY_HOME)

        def getmouse_error():
            raise curses.error()
        with patch("curses.getmouse", new=getmouse_error):
            parent.get_input()
            self.assertIsNotNone(parent._last_event)
            self.assertEqual(parent._last_event.type, widgets.Event.TYPE_KEY)

    def test_default_event_handlers(self):
        parent, child = self.windows()

        pre = vars(parent)
        parent.text_event(widgets.Event.text_event("x"))
        self.assertEqual(pre, vars(parent))

        pre = vars(parent)
        parent.key_event(widgets.Event.key_event(123))
        self.assertEqual(pre, vars(parent))

        self.assertFalse(parent.window.resized)
        bounds = geo.Rect(x1=1, y1=2, x2=11, y2=22)
        parent.resize_event(widgets.Event.resize_event(bounds))
        self.assertEqual(parent.window_bounds(), bounds)
        self.assertTrue(parent.window.resized)
        parent.window.resized = False
        parent.resize_event(widgets.Event.resize_event(bounds))
        self.assertFalse(parent.window.resized)

        self.assertFalse(child.has_focus())
        child.mouse_event(widgets.Event.mouse_event(geo.Point(), 0))
        self.assertTrue(child.has_focus())

        self.assertFalse(parent.window.refreshed)
        parent.focus_event(widgets.Event.focus_event(True))
        self.assertTrue(parent.window.refreshed)
        parent.window.refreshed = False
        parent.focus_event(widgets.Event.focus_event(False))
        self.assertFalse(parent.window.refreshed)

    def test_event_change_focus_child(self):
        parent, child = self.windows()
        self.assertTrue(parent.event_change_focus_child(child))
        self.assertIs(parent.focus_child, child)

    def test_event_change_focus_child(self):
        parent, child = self.windows()

        self.assertFalse(parent.window.refreshed)
        self.assertFalse(child.window.refreshed)
        parent.refresh()
        self.assertTrue(parent.window.refreshed)
        self.assertTrue(child.window.refreshed)

        parent.window.refreshed = False
        child.window.refreshed = False
        child.active = False
        parent.refresh()
        self.assertTrue(parent.window.refreshed)
        self.assertFalse(child.window.refreshed)

    @patch("curses.newwin", new=lambda *args: MockCursesWindow(*args))
    def test_loop(self):
        widget = widgets.Widget(None)
        widget._renders = 0
        def render():
            widget._renders += 1
            if widget._renders > 4:
                raise Exception("Too many iterations")
        widget.render = render
        widget.window.input_queue = [
            curses.KEY_MOUSE,
            curses.KEY_MOUSE,
            curses.KEY_MOUSE,
            ord("q")
        ]
        widget.text_event = lambda *args: widget.deactivate()
        widget.loop()
        self.assertTrue(widget.window.refreshed)
        self.assertEqual(widget._renders, 4)


class TestWidgetEvent(test_common.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWidgetEvent, self).__init__(*args, **kwargs)

        with patch("curses.newwin", new=lambda *args: MockCursesWindow(*args)):
            self.parent = widgets.Widget(None)
            self.child = widgets.Widget(self.parent)
            self.sibling = widgets.Widget(self.parent)

        self.resize_event= CaptureEvent(self.parent, "resize_event")
        self.text_event  = CaptureEvent(self.parent, "text_event")
        self.key_event   = CaptureEvent(self.parent, "key_event")
        self.mouse_event = CaptureEvent(self.parent, "mouse_event")
        self.focus_event = CaptureEvent(self.parent, "focus_event")

        self.child_resize_event= CaptureEvent(self.child, "resize_event")
        self.child_text_event  = CaptureEvent(self.child, "text_event")
        self.child_key_event   = CaptureEvent(self.child, "key_event")
        self.child_mouse_event = CaptureEvent(self.child, "mouse_event")
        self.child_focus_event = CaptureEvent(self.child, "focus_event")

        self.sibling_resize_event= CaptureEvent(self.sibling, "resize_event")
        self.sibling_text_event  = CaptureEvent(self.sibling, "text_event")
        self.sibling_key_event   = CaptureEvent(self.sibling, "key_event")
        self.sibling_mouse_event = CaptureEvent(self.sibling, "mouse_event")
        self.sibling_focus_event = CaptureEvent(self.sibling, "focus_event")

    def setUp(self):
        self.parent.active = self.child.active = True
        self.parent.focus(self.child)

        self.resize_event.propagate = True
        self.text_event.propagate = True
        self.key_event.propagate = True
        self.mouse_event.propagate = True
        self.focus_event.propagate = True

        self.child_resize_event.propagate = True
        self.child_text_event.propagate = True
        self.child_key_event.propagate = True
        self.child_mouse_event.propagate = True
        self.child_focus_event.propagate = True

        self.sibling_resize_event.propagate = True
        self.sibling_text_event.propagate = True
        self.sibling_key_event.propagate = True
        self.sibling_mouse_event.propagate = True
        self.sibling_focus_event.propagate = True

        self.parent._captured_events = []
        self.child._captured_events = []
        self.sibling._captured_events = []

    def no_focus(self):
        self.parent.focus(None)
        self.child._captured_events = []
        self.sibling._captured_events = []

    def test_not_active(self):
        self.parent.active = False
        self.parent.event(widgets.Event.resize_event(geo.Rect()))
        self.parent.event(widgets.Event.text_event("x"))
        self.parent.event(widgets.Event.key_event(123))
        self.parent.event(widgets.Event.mouse_event(geo.Point(), 123))
        self.parent.event(widgets.Event.focus_event(False))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(self.parent._captured_events[0][0], "resize_event")
        self.parent.active = True

    def test_unknown_event(self):
        self.parent.event(widgets.Event(-1))
        self.assertEqual(self.parent._captured_events, [])

    def test_focus(self):
        self.parent.event(widgets.Event.focus_event(False))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "focus_event")
        self.assertEqual(self.parent._captured_events[0][1].focus, False)

    def test_key_nofocus(self):
        self.no_focus()
        self.parent.event(widgets.Event.key_event(123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "key_event")
        self.assertEqual(self.parent._captured_events[0][1].key, 123)

    def test_key_propagate(self):
        self.parent.event(widgets.Event.key_event(123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 1)
        self.assertEqual(self.parent._captured_events[0][0], "key_event")
        self.assertEqual(self.parent._captured_events[0][1].key, 123)
        self.assertEqual(self.child._captured_events[0][0], "key_event")
        self.assertEqual(self.child._captured_events[0][1].key, 123)

    def test_key_nopropagate(self):
        self.key_event.propagate = False
        self.parent.event(widgets.Event.key_event(123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "key_event")
        self.assertEqual(self.parent._captured_events[0][1].key, 123)

    def test_text_nofocus(self):
        self.no_focus()
        self.parent.event(widgets.Event.text_event("1"))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "text_event")
        self.assertEqual(self.parent._captured_events[0][1].char, "1")

    def test_text_propagate(self):
        self.parent.event(widgets.Event.text_event("1"))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 1)
        self.assertEqual(self.parent._captured_events[0][0], "text_event")
        self.assertEqual(self.parent._captured_events[0][1].char, "1")
        self.assertEqual(self.child._captured_events[0][0], "text_event")
        self.assertEqual(self.child._captured_events[0][1].char, "1")

    def test_text_nopropagate(self):
        self.text_event.propagate = False
        self.parent.event(widgets.Event.text_event("1"))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "text_event")
        self.assertEqual(self.parent._captured_events[0][1].char, "1")

    def test_mouse_nopropagate(self):
        self.no_focus()
        self.mouse_event.propagate = False
        self.parent.event(widgets.Event.mouse_event(geo.Point(1, 2), 123))

        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)

        self.assertEqual(self.parent._captured_events[0][0], "mouse_event")
        self.assertEqual(self.parent._captured_events[0][1].pos, geo.Point(1, 2))
        self.assertEqual(self.parent._captured_events[0][1].buttons, 123)

        self.assertFalse(self.child.has_focus())

    def test_mouse_nofocus(self):
        self.no_focus()
        self.child_mouse_event.propagate = False
        self.parent.event(widgets.Event.mouse_event(geo.Point(1, 2), 123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 1)
        self.assertEqual(len(self.sibling._captured_events), 0)

        self.assertEqual(self.child._captured_events[0][0], "mouse_event")
        self.assertEqual(self.child._captured_events[0][1].pos, geo.Point(1, 2))
        self.assertEqual(self.child._captured_events[0][1].buttons, 123)

        self.assertTrue(self.child.has_focus())

    def test_mouse_propagate(self):
        self.parent.event(widgets.Event.mouse_event(geo.Point(1, 2), 123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 1)
        self.assertEqual(len(self.sibling._captured_events), 1)

        self.assertEqual(self.sibling._captured_events[0][0], "mouse_event")
        self.assertEqual(self.sibling._captured_events[0][1].pos, geo.Point(1, 2))
        self.assertEqual(self.sibling._captured_events[0][1].buttons, 123)

    def test_mouse_skip_inactive(self):
        self.child.active = False
        self.parent.event(widgets.Event.mouse_event(geo.Point(1, 2), 123))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(len(self.sibling._captured_events), 1)

    def test_mouse_deny_focus(self):
        self.no_focus()
        self.child_mouse_event.propagate = False
        with patch.object(self.parent, "event_change_focus_child", lambda x: False):
            self.parent.event(widgets.Event.mouse_event(geo.Point(1, 2), 123))
        self.assertFalse(self.child.has_focus())

    def test_resize_nopropagate(self):
        self.resize_event.propagate = False
        rect = geo.Rect(x=0, y=0, width=10, height=10)
        self.parent.event(widgets.Event.resize_event(rect))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 0)
        self.assertEqual(self.parent._captured_events[0][0], "resize_event")
        self.assertEqual(self.parent._captured_events[0][1].bounds, rect)

    def test_resize_propagate(self):
        rect = geo.Rect(x=0, y=0, width=10, height=10)
        self.parent.adjust_window_size(rect)
        self.parent.event(widgets.Event.resize_event(rect))
        self.assertEqual(len(self.parent._captured_events), 1)
        self.assertEqual(len(self.child._captured_events), 1)
        self.assertEqual(self.child._captured_events[0][0], "resize_event")
        self.assertEqual(self.child._captured_events[0][1].bounds, rect)


class CaptureEvent(object):
    def __init__(self, object, name, propagate=True):
        self.object = object
        self.name = name
        self.propagate = propagate
        self.object._captured_events = []
        setattr(self.object, name, self)

    def __call__(self, event):
        self.object._captured_events.append((self.name, event))
        event.propagate = self.propagate


class TestTabBar(test_common.TestCase):
    def setUp(self):
        self.widget = widgets.TabBar(
            None,
            MockCursesWindow(1, 64),
            ["foo", "bar", "baz"],
            None,
        )
        self.changed = []
        self.widget.signal_changed = self.changed.append

    def test_key_event(self):
        self.widget.window.input_queue = [
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_LEFT,
            curses.KEY_LEFT,
            curses.KEY_HOME,
            curses.KEY_END,
            curses.KEY_F1,
            ord("q"),
        ]

        with patch.object(self.widget, "text_event", lambda e: self.widget.deactivate()):
            self.widget.loop()
        self.assertEqual(self.changed, ["foo", "bar", "baz", "foo", "baz", "bar", "foo", "baz"])

        self.widget.items = []
        self.widget.current = "foo"
        self.widget.key_event(widgets.Event.key_event(curses.KEY_RIGHT))
        self.assertIsNone(self.widget.current)
        self.widget.current = "foo"
        self.widget.key_event(widgets.Event.key_event(curses.KEY_HOME))
        self.assertIsNone(self.widget.current)
        self.widget.current = "foo"
        self.widget.key_event(widgets.Event.key_event(curses.KEY_END))
        self.assertIsNone(self.widget.current)

    def test_window_bounds_hint(self):
        rect = geo.Rect(x=4, y=7, width=25, height=84)
        self.assertEqual(
            self.widget.window_bounds_hint(rect),
            geo.Rect(x=rect.x, y=rect.y, width=rect.width, height=1)
        )

    def test_mouse_event(self):
        event = widgets.Event.mouse_event(geo.Point(5, 0), curses.BUTTON2_CLICKED)
        self.widget.mouse_event(event)
        self.assertTrue(event.propagate)

        event.buttons = curses.BUTTON1_CLICKED
        self.widget.mouse_event(event)
        self.assertFalse(event.propagate)
        self.assertEqual(self.widget.current, "bar")

        event = widgets.Event.mouse_event(geo.Point(99, 0), curses.BUTTON1_CLICKED)
        self.widget.mouse_event(event)
        self.assertFalse(event.propagate)
        self.assertEqual(self.widget.current, "bar")

    def test_no_extra_switch(self):
        self.widget.window.input_queue = [
            curses.KEY_RIGHT,
            curses.KEY_HOME,
            ord("q"),
        ]
        with patch.object(self.widget, "text_event", lambda e: self.widget.deactivate()):
            self.widget.loop()
        self.assertEqual(self.changed, ["foo"])

    def test_default_action(self):
        self.widget = widgets.TabBar(
            None,
            MockCursesWindow(1, 64),
            ["foo", "bar", "baz"],
            None,
        )
        self.widget.window.input_queue = [
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_RIGHT,
            curses.KEY_LEFT,
            curses.KEY_LEFT,
            curses.KEY_HOME,
            curses.KEY_END,
            ord("q"),
        ]
        self.widget.text_event = lambda *args: self.widget.deactivate()
        self.widget.loop()

    def test_render(self):
        self.widget.current = self.widget.items[0]

        separator_string = (self.widget.separator, curses.A_NORMAL)
        strings = self.widget.window.strings

        self.widget.refresh()
        self.assertEqual(strings[(0, 0)], separator_string)
        self.assertEqual(strings[(1, 0)], ("foo", curses.A_REVERSE))
        self.assertEqual(strings[(4, 0)], separator_string)
        self.assertEqual(strings[(5, 0)], ("bar", curses.A_NORMAL))
        self.assertEqual(strings[(8, 0)], separator_string)
        self.assertEqual(strings[(9, 0)], ("baz", curses.A_NORMAL))
        self.assertEqual(strings[(12, 0)], separator_string)

        with patch.object(self.widget, "has_focus", new=lambda: False):
            self.widget.refresh()
            self.assertEqual(strings[(0, 0)], separator_string)
            self.assertEqual(strings[(1, 0)], ("foo", curses.A_UNDERLINE))
            self.assertEqual(strings[(4, 0)], separator_string)
            self.assertEqual(strings[(5, 0)], ("bar", curses.A_NORMAL))
            self.assertEqual(strings[(8, 0)], separator_string)
            self.assertEqual(strings[(9, 0)], ("baz", curses.A_NORMAL))
            self.assertEqual(strings[(12, 0)], separator_string)


class TestMenu(test_common.TestCase):
    class Item(widgets.Menu.Item):
        def __init__(self, name, test_obj):
            super(TestMenu.Item, self).__init__(name)
            self.action = lambda: test_obj.activated.append(name)

    def setUp(self):
        self.activated = []
        self.widget = widgets.Menu(
            None,
            MockCursesWindow(24, 80),
            [
                TestMenu.Item("foo", self),
                TestMenu.Item("bar", self),
                TestMenu.Item("baz", self),
            ],
        )

    def test_ctor(self):
        self.assertIs(self.widget.current, self.widget.items[0])

        other = widgets.Menu(None, MockCursesWindow(24, 80))
        self.assertIsNone(other.current)

    def test_window_bounds_hint(self):
        self.assertEqual(
            self.widget.window_bounds_hint(geo.Rect(x1=1, y1=2, x2=116, y2=92)),
            geo.Rect(x=100, y=2, width=16, height=90),
        )

    def test_key_events(self):
        self.widget.window.input_queue = [
            curses.KEY_DOWN,
            curses.KEY_ENTER,
            curses.KEY_DOWN,
            curses.KEY_ENTER,
            ord(" "),
            curses.KEY_DOWN,
            curses.KEY_ENTER,
            curses.KEY_DOWN,
            curses.KEY_ENTER,
            curses.KEY_UP,
            curses.KEY_UP,
            ord(" "),
            curses.KEY_HOME,
            ord(" "),
            curses.KEY_END,
            ord(" "),
            curses.KEY_LEFT,
            ord("f"),
            ord("q"),
        ]

        old_te = self.widget.text_event
        def new_te(ev):
            if ev.char == "q":
                self.widget.deactivate()
            else:
                old_te(ev)

        self.widget.current = None
        with patch.object(self.widget, "text_event", new_te):
            self.widget.loop()

        self.assertEqual(
            self.activated,
            ["foo", "bar", "bar", "baz", "foo", "bar", "foo", "baz"]
        )

    def test_key_events_noitems(self):
        self.widget.items = []

        self.widget.current = 1
        self.widget.key_event(widgets.Event.key_event(curses.KEY_HOME))
        self.assertIsNone(self.widget.current)

        self.widget.current = 1
        self.widget.key_event(widgets.Event.key_event(curses.KEY_END))
        self.assertIsNone(self.widget.current)

        self.widget.current = 1
        self.widget.key_event(widgets.Event.key_event(curses.KEY_UP))
        self.assertIsNone(self.widget.current)

        self.widget.current = 1
        self.widget.key_event(widgets.Event.key_event(curses.KEY_DOWN))
        self.assertIsNone(self.widget.current)

    def test_activate(self):
        self.widget.activate()
        self.assertEqual(self.activated, ["foo"])

        self.activated = []
        self.widget.current = None
        self.widget.activate()
        self.assertEqual(self.activated, [])

    def test_submenu(self):
        sub1 = [
            TestMenu.Item("a1", self),
            TestMenu.Item("a2", self),
            TestMenu.Item("a3", self),
        ]
        sub2 = [
            TestMenu.Item("b1", self),
            TestMenu.Item("b2", self),
            TestMenu.Item("b3", self),
        ]
        sub3 = []

        self.widget.push_submenu(sub1)
        self.assertIn(self.widget.current, sub1)
        self.assertEqual(self.widget.items, sub1)

        self.widget.push_submenu(sub2)
        self.assertIn(self.widget.current, sub2)
        self.assertEqual(self.widget.items, sub2)

        self.widget.push_submenu(sub3)
        self.assertIsNone(self.widget.current)
        self.assertEqual(self.widget.items, [])

        self.widget.pop_submenu()
        self.assertIn(self.widget.current, sub2)
        self.assertEqual(self.widget.items, sub2)

        self.widget.key_event(widgets.Event.key_event(curses.KEY_BACKSPACE))
        self.assertIn(self.widget.current, sub1)
        self.assertEqual(self.widget.items, sub1)

        self.widget.key_event(widgets.Event.key_event(curses.KEY_BACKSPACE))
        self.widget.key_event(widgets.Event.key_event(curses.KEY_BACKSPACE))
        self.assertNotEqual(self.widget.items, sub1)
        self.assertEqual(len(self.widget.items), 3)

        self.assertRaises(OverflowError, self.widget.pop_submenu)

    def test_focus_event(self):
        self.widget.current = None

        self.widget.focus_event(widgets.Event.focus_event(False))
        self.assertIsNone(self.widget.current)

        self.widget.focus_event(widgets.Event.focus_event(True))
        self.assertIn(self.widget.current, self.widget.items)

        self.widget.focus_event(widgets.Event.focus_event(False))
        self.assertIn(self.widget.current, self.widget.items)

        self.widget.current = None
        self.widget.items = []
        self.widget.focus_event(widgets.Event.focus_event(True))
        self.assertIsNone(self.widget.current)

    def test_auto_activate(self):
        self.widget.items[0].auto_activate = True
        self.widget.items[2].auto_activate = True
        self.widget.current = None


        self.widget.window.input_queue = [
            curses.KEY_DOWN,
            curses.KEY_DOWN,
            curses.KEY_DOWN,
            ord("q")
        ]

        self.widget.current = None
        with patch.object(self.widget, "text_event",
                          lambda x: self.widget.deactivate()):
            self.widget.loop()

        self.assertEqual(self.activated, ["foo", "baz"])

    def test__starting_y(self):
        with patch.object(self.widget, "window_bounds",
                return_value=geo.Rect(x=100, y=100, width=10, height=3)):
            self.assertEqual(self.widget._starting_y(), 100)

        with patch.object(self.widget, "window_bounds",
                return_value=geo.Rect(x=100, y=200, width=10, height=5)):
            self.assertEqual(self.widget._starting_y(), 201)

        with patch.object(self.widget, "window_bounds",
                return_value=geo.Rect(x=0, y=0, width=80, height=24)):
            self.assertEqual(self.widget._starting_y(), int((24-3)/2))

    def test_render(self):
        self.widget.current = self.widget.items[0]

        strings = self.widget.window.strings

        self.widget.refresh()
        starting_y = self.widget._starting_y()
        self.assertEqual(strings[(1, starting_y)], ("foo", curses.A_REVERSE))
        self.assertEqual(strings[(1, starting_y+1)], ("bar", curses.A_NORMAL))
        self.assertEqual(strings[(1, starting_y+2)], ("baz", curses.A_NORMAL))

        with patch.object(self.widget, "has_focus", new=lambda: False):
            self.widget.refresh()
            self.assertEqual(strings[(1, starting_y)], ("foo", curses.A_UNDERLINE))
            self.assertEqual(strings[(1, starting_y+1)], ("bar", curses.A_NORMAL))
            self.assertEqual(strings[(1, starting_y+2)], ("baz", curses.A_NORMAL))

    def test_mouse_event(self):
        self.widget.current = None
        ev = widgets.Event.mouse_event(
            geo.Point(1, self.widget._starting_y() + 1),
            curses.BUTTON1_CLICKED
        )
        self.widget.mouse_event(ev)
        self.assertIs(self.widget.current, self.widget.items[1])
        self.assertFalse(ev.propagate)

        ev = widgets.Event.mouse_event(
            geo.Point(1, 0),
            curses.BUTTON1_CLICKED
        )
        self.widget.mouse_event(ev)
        self.assertIs(self.widget.current, self.widget.items[1])
        self.assertFalse(ev.propagate)

        self.widget.current = None
        ev = widgets.Event.mouse_event(
            geo.Point(1, self.widget._starting_y() + 1),
            curses.BUTTON2_CLICKED
        )
        self.widget.mouse_event(ev)
        self.assertIsNone(self.widget.current)
        self.assertTrue(ev.propagate)

    def test_default_action(self):
        item = widgets.Menu.Item("hello")
        self.assertTrue(callable(item.action))
        item.action()


class TestTabWidget(test_common.TestCase):
    def setUp(self):
        self.widget = widgets.TabWidget(
            None,
            MockCursesWindow(24, 80),
            lambda wid: getattr(wid, "name", "Unnamed Widget")
        )

    def _create_tab(self, name):
        widget = self.widget.create_tab(widgets.Widget)
        widget.name = name
        return widget

    def _create_tabs(self, names=["foo", "bar", "baz"]):
        return [self._create_tab(name) for name in names]


    def test_container_area(self):
        self.assertEqual(
            self.widget.container.window_bounds(),
            geo.Rect(x=0, y=1, width=80, height=23)
        )

    def test_create_tab_noadd(self):
        widget = self.widget.create_tab_noadd()
        self.assertIsInstance(widget, widgets.Widget)
        self.assertNotIn(widget, self.widget.tabs)
        self.assertEqual(len(self.widget.tabs), 0)

    def test_create_tab(self):
        widget = self.widget.create_tab()
        self.assertIsInstance(widget, widgets.Widget)
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertIn(widget, self.widget.tabs)
        self.assertIs(widget, self.widget.current_tab)
        self.assertIs(widget, self.widget.bar.current)

    def test_add_tab(self):
        widget = self.widget.create_tab_noadd()
        self.assertIsInstance(widget, widgets.Widget)
        self.assertNotIn(widget, self.widget.tabs)

        self.widget.add_tab(widget)
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertIn(widget, self.widget.tabs)
        self.assertIs(widget, self.widget.current_tab)
        self.assertIs(widget, self.widget.bar.current)

        self._create_tab("foo")
        self.widget.add_tab(widget)
        self.widget.add_tab(widget)
        self.assertEqual(len(self.widget.tabs), 2)

    def test__switch_current(self):
        tabs = self._create_tabs()
        self.assertEqual(tabs, self.widget.tabs)
        self.widget._switch_current(tabs[1])
        self.assertIs(tabs[1], self.widget.current_tab)
        self.assertIs(tabs[1], self.widget.bar.current)
        self.assertFalse(tabs[0].active)
        self.assertTrue(tabs[1].active)
        self.assertFalse(tabs[2].active)
        self.assertTrue(self.widget.window.refreshed)

        self.widget.window.refreshed = False
        self.widget._switch_current(tabs[1])
        self.assertFalse(self.widget.window.refreshed)

        self.widget._switch_current(None)
        self.assertIsNone(self.widget.current_tab)
        self.assertIsNone(self.widget.bar.current)

        self.widget._switch_current(tabs[1])
        self.assertIs(tabs[1], self.widget.current_tab)
        self.assertIs(tabs[1], self.widget.bar.current)

    def test_close_current(self):
        tabs = self._create_tabs()
        self.widget._switch_current(tabs[1])
        self.widget.close_current()
        self.assertIs(tabs[2], self.widget.current_tab)
        self.assertEqual(len(self.widget.tabs), 2)

        self.widget.current_tab = None
        self.widget.close_current()
        self.assertEqual(len(self.widget.tabs), 2)

        self.widget.current_tab = tabs[2]
        self.widget.close_current()
        self.assertIs(tabs[0], self.widget.current_tab)
        self.assertEqual(len(self.widget.tabs), 1)

        self.widget.close_current()
        self.assertIsNone(self.widget.current_tab)
        self.assertEqual(len(self.widget.tabs), 0)

        self.widget.close_current()

    def test_formatter(self):
        tabs = self._create_tabs()
        self.assertEqual(self.widget.bar.formatter(tabs[0]), "foo")

        self.widget = widgets.TabWidget(
            None,
            MockCursesWindow(24, 80),
        )
        tabs = self._create_tabs()
        self.assertEqual(self.widget.bar.formatter(tabs[0]), "tab")

    def test_on_activated(self):
        self.widget._activated = None

        def on_activated(tab):
            self.widget._activated = tab

        with patch.object(self.widget, "on_activated", on_activated):
            tabs = self._create_tabs()
            self.widget._activated = None
            self.widget.activate_tab()
            self.assertIs(self.widget._activated, tabs[2])

            self.widget._switch_current(None)
            self.widget.activate_tab()
            self.assertIs(self.widget._activated, tabs[2])


test_common.main()
