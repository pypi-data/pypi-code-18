from collections import namedtuple
from time import monotonic

from .screen import Screen
from .terminal import write

Point = namedtuple("Point", ("x", "y"))
Rectangle = namedtuple("Rectangle", ("x1", "y1", "x2", "y2"))


class Points:
    def __init__(self, limit=None):
        self.limit = limit

        self._ps = []
        self._min_x = None
        self._min_y = None
        self._max_x = None
        self._max_y = None

    def _update(self, p):
        if self._min_x is None:
            self._min_x = p.x
        elif self._min_x > p.x:
            self._min_x = p.x

        if self._min_y is None:
            self._min_y = p.y
        elif self._min_y > p.y:
            self._min_y = p.y

        if self._max_x is None:
            self._max_x = p.x
        elif self._max_x < p.x:
            self._max_x = p.x

        if self._max_y is None:
            self._max_y = p.y
        elif self._max_y < p.y:
            self._max_y = p.y

    def _recalculate_bounds(self):
        self._min_x = None
        self._min_y = None
        self._max_x = None
        self._max_y = None
        for p in self._ps:
            self._update(p)

    def _over_limit(self):
        return self.limit is not None and len(self._ps) > self.limit

    def _remove_extra(self):
        self._ps[:] = self._ps[len(self._ps) - self.limit:]
        self._recalculate_bounds()

    def add(self, p):
        self._ps.append(p)

        if self._over_limit():
            self._remove_extra()
        else:
            self._update(p)

    def extend(self, ps):
        self._ps.extend(ps)

        if self._over_limit():
            self._remove_extra()
        else:
            for p in self._ps[-len(ps):]:
                self._update(p)

    def points(self):
        for p in self._ps:
            yield p

    def bounds(self, b=None):
        if len(self._ps) > 0:
            assert(4 == len(list(
                filter(lambda x: x is not None, (
                    self._min_x, self._min_y,
                    self._max_x, self._max_y)))))
        elif len(self._ps) == 0:
            return Rectangle(0, 0, 0, 0)

        if b is None:
            b = Rectangle(None, None, None, None)

        return Rectangle(
            self._min_x if b.x1 is None else b.x1,
            self._min_y if b.y1 is None else b.y1,
            self._max_x if b.x2 is None else b.x2,
            self._max_y if b.y2 is None else b.y2)


class PPGR:
    def __init__(self, format, fail_bad_line=False, wait=None, time_scale=None, limit=None):
        self.format = format
        self.fail_bad_line = fail_bad_line
        self.ps = Points(limit)

        self.wait = wait
        if self.wait is not None:
            self.wait /= 1000

        self.time_scale = time_scale
        if self.time_scale is None:
            self.t0 = monotonic()

        self.screen = Screen()
        self.t = 0

    def _prep_screen(self, max_x=None, min_x=None, max_y=None, min_y=None):
        """preps the canvas so that it can be drawn"""

        def f(l1, l2):
            try:
                return l1 / l2
            except ZeroDivisionError:
                return 1

        def scale(p):
            """Tranform point p from internal coordinates to screen coordinates."""

            return Point(
                fact.x * (p.x - bounds.x1),
                size.y - fact.y * (p.y - bounds.y1))

        self.screen.size = None, None
        size = Point(*self.screen.size)
        bounds = self.ps.bounds(Rectangle(min_x, min_y, max_x, max_y))
        fact = Point(
            f(size.x, abs(bounds.x1 - bounds.x2)),
            f(size.y, abs(bounds.y1 - bounds.y2)))

        for p in map(scale, self.ps.points()):
            self.screen(*p)

    def _update_t(self):
        if self.time_scale is None:
            self.t = monotonic() - self.t0
        else:
            self.t += self.time_scale

    def line(self, line):
        # TODO better error handling
        # TODO better support for --fail-bad-line
        # TODO add support for histograms (difficult?)
        f = {
            "a": lambda a: f["d"](a) if len(a) >= 2 else f["t"](a),
            "t": lambda a: Point(self.t, a.pop()),
            "d": lambda a: Point(a.pop(), a.pop())}

        _line = line

        try:
            line = list(map(float, line.strip().split()))
        except (ValueError, TypeError) as e:
            if self.fail_bad_line:
                raise Exception("bad line: {}".format(_line))
            else:
                return

        a = list(reversed(line))

        out = []
        for i in self.format:
            try:
                if i == "s":
                    a.pop()
                    continue
                out.append(f[i](a))
            except IndexError as e:
                if self.fail_bad_line:
                    raise Exception("bad line: {} failed".format(_line))

        self.ps.extend(out)
        self._update_t()

    def show(self, max_x=None, min_x=None, max_y=None, min_y=None, no_animate=False, newline=False):
        self._prep_screen(max_x, min_x, max_y, min_y)
        write(
            self.screen,
            wait=None if no_animate else self.wait,
            end="\n" if newline else "")
