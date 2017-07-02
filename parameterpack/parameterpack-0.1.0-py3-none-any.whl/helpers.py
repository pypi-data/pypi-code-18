import itertools
import functools


def advance(n, iterator):
    try:
        for _ in range(n):
            next(iterator)
    except StopIteration:
        pass

    return iterator


def sliding_window(sequence, size=2):
    iterators = itertools.tee(sequence, size)

    stairstep = itertools.starmap(advance, enumerate(iterators))

    return zip(*stairstep)


def reduce_right(function, iterable, initial=None):
    """op, xs, x -> op(x, op(xs[0], op(xs[1], ...)))"""
    iterator = reversed(iterable)

    if initial is None:
        try:
            value = next(iterator)
        except StopIteration:
            value = initial
    else:
        value = initial

    for element in iterator:
        value = function(element, value)

    return value


def left_op(operator, comparison=False, identity=None):
    @functools.wraps(operator)
    def wrapper(self, other):
        if other is Ellipsis:
            if comparison:
                return self.apply_comparison(operator)

            return self.apply(operator, identity=identity)

        return NotImplemented

    return wrapper


def right_op(operator):
    @functools.wraps(operator)
    def wrapper(self, other):
        if other is Ellipsis:
            return self.apply_right(operator)

        return NotImplemented

    return wrapper


