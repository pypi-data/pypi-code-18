"""Testing Library for Runaway."""


# [ Imports ]
import sys


# [ API ]
def assertEqual(first, second):
    """Assert equality."""
    if first != second:
        raise AssertionError(f'{first} != {second}')


class TestWrapper:

    UNSET = object()

    def __init__(self, coro):
        self._coro = coro
        self._signal = self.UNSET
        self._returned = self.UNSET
        self._error = self.UNSET
        self._traceback = self.UNSET
        self.is_started()

    def is_started(self):
        self.receives_value(None)

    @property
    def signal(self):
        if self._returned is not self.UNSET:
            raise RuntimeError("Coro already returned")
        if self._error is not self.UNSET:
            raise RuntimeError("Error was raised.") from self._error.with_traceback(self._traceback)
        if self._signal is self.UNSET:
            raise RuntimeError("Signal not yet set.")
        to_return = self._signal
        self._signal = self.UNSET
        return to_return

    @property
    def error(self):
        if self._error is self.UNSET:
            raise RuntimeError("No error raised.")
        return self._error

    @property
    def returned(self):
        if self._error is not self.UNSET:
            raise RuntimeError("Error was raised.") from self._error.with_traceback(self._traceback)
        if self._returned is self.UNSET:
            raise RuntimeError("Coro has not yet returned.")
        return self._returned

    def receives_error(self, *exc_info):
        try:
            self._signal = self._coro.throw(*exc_info)
        except StopIteration as e:
            self._returned = e.value
        except GeneratorExit:
            self._returned = None
        except:
            _type, error, traceback = sys.exc_info()
            self._error = error
            self._traceback = traceback

    def receives_value(self, value):
        try:
            self._signal = self._coro.send(value)
        except StopIteration as e:
            self._returned = e.value
        except:
            _type, error, traceback = sys.exc_info()
            self._error = error
            self._traceback = traceback
