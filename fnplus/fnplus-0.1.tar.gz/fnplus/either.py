from typing import Any, TypeVar, Generic, Union
from functools import partial

from .monad import Func, Monad

T = TypeVar('T')


class Either(Monad, Generic[T]):
    def __init__(self, value: T, error: Exception=None):
        super().__init__(value)
        self._error = error or None

    def get_error(self) -> Union[Exception, None]:
        return self._error

    def _bind(self, f: Func) -> 'Either':
        if self._error is not None or self._value is None:
            return self
        return Either(f(self._value))

    def _try_bind(self, f: Func) -> 'Either':
        try:
            return self._bind(f)
        except Exception as e:
            return Either(None, e)

    @staticmethod
    def try_(f: Func):
        def _inner(f: Func, x: Any=None):
            try:
                value = f(x) if x else f()
                return Either(value)
            except Exception as e:
                return Either(None, e)

        return partial(_inner, f)

    @staticmethod
    def try_bind(f: Func) -> Func:
        def _inner(f: Func, either: Either):
            return either._try_bind(f)

        return partial(_inner, f)
