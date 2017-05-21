"""
This module overrides the Range.__and__ function, so that it returns a boolean value
based on if the two objects overlap.

The rationale behind this is that it mirrors the `range && range` operator in postgres.

There are tests for this, that hit the database with randomly generated ranges and ensure
that the database and this method agree upon the results.

There is also a more complete `isempty()` method, which examines the bounds types and values,
and determines if the object is indeed empty. This is required when python-created range objects
are dealt with, as these are not normalised the same way that postgres does.
"""
import datetime
from psycopg2.extras import Range


OFFSET = {
    int: 1,
    datetime.date: datetime.timedelta(1),
}


def normalise(instance):
    """
    In the case of discrete ranges (integer, date), then we normalise the values
    so it is in the form [start,finish), the same way that postgres does.

    If the lower value is None, we normalise this to (None,finish)
    """
    if instance.isempty:
        return instance

    lower = instance.lower
    upper = instance.upper
    bounds = list(instance._bounds)

    if lower is not None and lower == upper and instance._bounds != '[]':
        return instance.__class__(empty=True)

    if lower is None:
        bounds[0] = '('
    elif bounds[0] == '(' and type(lower) in OFFSET:
        lower += OFFSET[type(lower)]
        bounds[0] = '['

    if upper is None:
        bounds[1] = ')'
    elif bounds[1] == ']' and type(upper) in OFFSET:
        upper += OFFSET[type(upper)]
        bounds[1] = ')'

    if lower is not None and lower == upper and bounds != ['[', ']']:
        return instance.__class__(empty=True)

    return instance.__class__(lower, upper, ''.join(bounds))


def __and__(self, other):
    if not isinstance(other, self.__class__):
        raise TypeError("unsupported operand type(s) for &: '{}' and '{}'".format(
            self.__class__.__name__, other.__class__.__name__
        ))

    self = normalise(self)
    other = normalise(other)

    # If _either_ object is empty, then it will never overlap with any other one.
    if self.isempty or other.isempty:
        return False

    if other < self:
        return other & self

    # Because we can't compare None with a datetime.date(), we need to deal
    # with the cases where one (or both) of the parts are None first.
    if self.lower is None:
        if self.upper is None or other.lower is None:
            return True
        if self.upper_inc and other.lower_inc:
            return self.upper >= other.lower
        return self.upper > other.lower

    if self.upper is None:
        if other.upper is None:
            return True
        if self.lower_inc and other.upper_inc:
            return self.lower <= other.upper
        return self.lower < other.upper

    # Now, all we care about is self.upper_inc and other.lower_inc
    if self.upper_inc and other.lower_inc:
        return self.upper >= other.lower
    else:
        return self.upper > other.lower


def __eq__(self, other):
    if not isinstance(other, Range):
        return False

    self = normalise(self)
    other = normalise(other)

    return (self._lower == other._lower and
            self._upper == other._upper and
            self._bounds == other._bounds)


Range.__and__ = __and__
Range.__eq__ = __eq__
