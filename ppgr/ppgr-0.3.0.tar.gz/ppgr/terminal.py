import sys

from contextlib import contextmanager


def write(s="", wait=None, clear=True, flush=True, end="", stream=sys.stdout):
    if clear:
        stream.write("\x1b[2J\x1b[H")
    stream.write(s + end)
    if flush:
        stream.flush()
    if wait is not None:
        time.sleep(wait)


@contextmanager
def no_cursor():
    write("\x1b[?25l", clear=False)
    try:
        yield
    finally:
        write("\x1b[?25h", clear=False)
