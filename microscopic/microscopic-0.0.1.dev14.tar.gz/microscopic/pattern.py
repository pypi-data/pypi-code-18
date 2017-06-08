from typing import Generator, Optional, Tuple, Union

import regex


class PatternContext:
    def __init__(self, pattern: Union[bytes, bytearray], *, chunk_size: int):
        self._sre = regex.compile(pattern)
        self._state = None
        self._dirty = False
        self.chunk_size = chunk_size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return

        if self._dirty:
            raise RuntimeError('dirty context was not drained')

    def __repr__(self):
        name = self.__class__.__module__ + '.' + self.__class__.__qualname__
        dirty = ' [dirty]' if self._dirty else ''

        return "<{name} pattern={pattern} chunk_size={chunk_size}{dirty}>".format(
            name=name,
            pattern=self._sre.pattern,
            chunk_size=self.chunk_size,
            dirty=dirty)

    def _resume(self, buf: Union[bytes, bytearray]):
        if self._state is None:
            return buf

        _buf = bytearray(self._state)
        _buf.extend(buf)
        self._state = None
        return _buf

    def _suspend(self, buf: Union[bytes, bytearray]):
        self._state = buf

    def feed(self, buf: Union[bytes, bytearray]) -> Generator[Tuple[Optional[memoryview], Optional[memoryview]], None, None]:
        """
        Yields::
            (split, match)

        """
        self._dirty = True
        buf = self._resume(buf)

        view = memoryview(buf)
        view_length = len(view)
        last = 0
        for match in self._sre.finditer(view, partial=True, concurrent=True):
            start, end = match.span()

            if end == view_length:
                if last == 0 and end > self.chunk_size:
                    # reject matches that exceed chunk_size
                    continue

                # this match might be incomplete, depending the next buf
                if start != end:
                    self._suspend(view[start:end])
                if last != start:
                    yield view[last:start], None
                raise StopIteration

            yield view[last:start], view[start:end]

            last = end

        if last != view_length:
            yield view[last:view_length], None

    def drain(self) -> Tuple[Optional[Union[bytes, bytearray]], Optional[Union[bytes, bytearray]]]:
        """
        Returns::
            (split, match)

        """
        self._dirty = False
        state = self._state
        self._state = None

        if not state:
            return (None, None)
        if self._sre.match(state, concurrent=True):
            return (None, state)
        return (state, None)
