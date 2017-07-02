import itertools
import functools
import operator
from .helpers import left_op, right_op, reduce_right, sliding_window

import sys

PY35 = sys.version_info >= (3, 5)

__version__ = "0.1.0"


def pack(*args):
    return ParameterPack(*args)


class ParameterPack:
    __slots__ = ('items',)

    def __init__(self, *items):
        self.items = items

    def __repr__(self) -> str:
        return '{}{}'.format(type(self).__name__, repr(self.items))

    def __str__(self) -> str:
        return str(self.items) + '...'

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)

    def apply(self, operator, identity=None):
        if len(self.items) == 0:
            return identity

        if len(self.items) == 1:
            return self.items[0]

        return functools.reduce(operator, self.items[1:], self.items[0])

    def apply_right(self, operator, identity=None):
        if len(self.items) == 0:
            return identity

        return reduce_right(operator, self.items)

    def apply_comparison(self, operator):
        # If every comparison returned True, return the last element of the pack to support comparison chaining.
        if all(itertools.starmap(operator, sliding_window(self.items))):
            return self.items[-1]

        # If any comparison returned False, the entire comparison chain should return False as well. To enforce this,
        # we return an object that always returns False when compared in any way with anything.
        return FalseComparison()

    def __call__(self, *args, **kwargs):
        index = None

        for i, arg in enumerate(args):
            if arg is Ellipsis:
                index = i
                break

        if index is None:
            raise NotImplemented

        def prepare_args(x):
            return args[:index] + (x,) + args[index + 1:]

        return functools.reduce(lambda xs, x: xs(*prepare_args(x), **kwargs), self.items)

    __add__ = left_op(operator.add)
    __sub__ = left_op(operator.sub)
    __mul__ = left_op(operator.mul)
    __floordiv__ = left_op(operator.floordiv)
    __truediv__ = left_op(operator.truediv)
    __mod__ = left_op(operator.mod)
    __and__ = left_op(operator.and_)
    __or__ = left_op(operator.or_)
    __xor__ = left_op(operator.xor)
    __lshift__ = left_op(operator.lshift)
    __rshift__ = left_op(operator.rshift)

    __eq__ = left_op(operator.eq, comparison=True)
    __ne__ = left_op(operator.ne, comparison=True)
    __lt__ = left_op(operator.lt, comparison=True)
    __le__ = left_op(operator.le, comparison=True)
    __gt__ = left_op(operator.gt, comparison=True)
    __ge__ = left_op(operator.ge, comparison=True)

    __radd__ = right_op(operator.add)
    __rsub__ = right_op(operator.sub)
    __rmul__ = right_op(operator.mul)
    __rfloordiv__ = right_op(operator.floordiv)
    __rtruediv__ = right_op(operator.truediv)
    __rmod__ = right_op(operator.mod)
    __rand__ = right_op(operator.and_)
    __ror__ = right_op(operator.or_)
    __rxor__ = right_op(operator.xor)
    __rlshift__ = right_op(operator.lshift)
    __rrshift__ = right_op(operator.rshift)

    if PY35:
        __matmul__ = left_op(operator.matmul)
        __rmatmul__ = right_op(operator.matmul)


def nope(*args, **kwargs):
    return False


class FalseComparison:
    __lt__ = nope
    __le__ = nope
    __gt__ = nope
    __ge__ = nope
    __eq__ = nope
    __ne__ = nope

    __bool__ = nope
