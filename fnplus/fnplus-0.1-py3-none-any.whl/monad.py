from functools import partial
from typing import Callable, Any, Generic, TypeVar
from abc import ABCMeta, abstractmethod

T = TypeVar('T')
Func = Callable[[T], Any]


class Monad(Generic[T]):
    __metaclass__ = ABCMeta

    def __init__(self, value: T):
        self._value = value or None

    def get_value(self) -> T:
        return self._value

    @abstractmethod
    def _bind(self, f: Func) -> 'Monad': pass

    @staticmethod
    def bind(fn: Func) -> Func:
        def __inner(fn: Func, monad: Monad):
            return monad._bind(fn)

        return partial(__inner, fn)
