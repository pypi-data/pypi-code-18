import time
import sys

from contextlib import contextmanager
from collections import namedtuple

from .screen import Screen, terminal_size


Point = namedtuple("Point", ("x", "y"))


def write_stdout(s="", wait=None, clear=True, flush=True, end=""):
    if clear:
        sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.write(s + end)
    if flush:
        sys.stdout.flush()
    if wait is not None:
        time.sleep(wait)


@contextmanager
def no_cursor():
    write_stdout("\x1b[?25l", clear=False)
    try:
        yield
    finally:
        write_stdout("\x1b[?25h", clear=False)


class PPGR:
    def __init__(self, format=None, fail_bad_line=False, wait=None, time_scale=None, limit=None):
        if format is None:
            format = ["a"]

        self.format = format
        self.fail_bad_line = fail_bad_line
        self.wait = wait
        if self.wait is not None:
            self.wait /= 1000
        self.time_scale = time_scale
        if self.time_scale is None:
            self._t0 = time.monotonic()
        self.limit = limit

        self._ps = []
        self._canvas = Screen(to_int=round)
        self._t = 0

        self._max_x = None
        self._min_x = None
        self._max_y = None
        self._min_y = None

    def _prep_canvas(self, max_x=None, min_x=None, max_y=None, min_y=None):
        if max_x is None:
            max_x = self._max_x
        if min_x is None:
            min_x = self._min_x

        if max_y is None:
            max_y = self._max_y
        if min_y is None:
            min_y = self._min_y

        w, h = terminal_size()

        try:
            x_fact = w / (max_x - min_x)
        except ZeroDivisionError:
            x_fact = 1

        try:
            y_fact = h / (max_y - min_y)
        except ZeroDivisionError:
            y_fact = 1

        out = []
        for i in self._ps:
            out.append(Point(
                (i.x - min_x) * x_fact,
                h - ((i.y - min_y) * y_fact)))

        self._canvas.size = None, None
        for p in out:
            self._canvas(*p)

        return out

    def line(self, line):
        line = map(float, line.strip().split())
        a = list(reversed(list(line)))

        # TODO: add support for histograms (difficult?)
        f = {
            "a": lambda a: f["d"](a) if len(a) >= 2 else f["t"](a),
            "t": lambda a: Point(self._t, a.pop()),
            "d": lambda a: Point(a.pop(), a.pop())}

        # we need to keep track of how many points are added
        many = 0
        for i in self.format:
            if i == "s":
                a.pop()
                continue
            self._ps.append(f[i](a))
            many += 1

        # keep track of mins and maxs while reading data
        # it's faster that calculcating mins and maxs everytime
        for i in range(many):
            last = self._ps[-(many)]

            if self._max_x is None:
                self._max_x = last.x
            if self._min_x is None:
                self._min_x = last.x

            if self._max_y is None:
                self._max_y = last.y
            if self._min_y is None:
                self._min_y = last.y


            if self._max_x < last.x:
                self._max_x = last.x
            if self._min_x > last.x:
                self._min_x = last.x

            if self._max_y < last.y:
                self._max_y = last.y
            if self._min_y > last.y:
                self._min_y = last.y

        if self.limit is not None:
            old_len = len(self._ps)

            # store at most limit points
            self._ps[:] = self._ps[len(self._ps) - self.limit:]

            # recalculate mins and maxs if the some items were removed
            if old_len > len(self._ps):
                self._max_x = max(map(lambda p: p.x, self._ps))
                self._min_x = min(map(lambda p: p.x, self._ps))
                self._max_y = max(map(lambda p: p.y, self._ps))
                self._min_y = min(map(lambda p: p.y, self._ps))

        if self.time_scale is None:
            self._t = time.monotonic() - self._t0
        else:
            self._t += self.time_scale

    def show(self, max_x=None, min_x=None, max_y=None, min_y=None, no_animate=False):
        self._prep_canvas(max_x, min_x, max_y, min_y)
        write_stdout(
            str(self._canvas),
            wait=None if no_animate else self.wait,
            end="\n")
