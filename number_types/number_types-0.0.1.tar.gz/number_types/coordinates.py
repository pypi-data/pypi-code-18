from __future__ import division

import math
import numbers

__all__ = ('Coordinate',)

math.tau = getattr(math, 'tau', 2 * math.pi)

class Coordinate(tuple):
    """
    An ordered pair of ordinals.

    Typically represents a point on a cartesian plane
    """
    def __new__(cls, x, y=None, is_rectangular=True):
        if y is None:
            x, y = x
        self = super(Coordinate, cls).__new__(Coordinate, (x, y))
        super(Coordinate, self).__init__()
        self._is_rectangular = bool(is_rectangular)
        return self

    @property
    def x(self):
        if self._is_rectangular:
            return self[0]
        raise TypeError('No `x` value on a polar coordinate!')

    @property
    def y(self):
        if self._is_rectangular:
            return self[1]
        raise TypeError('No `y` value on a polar coordinate!')

    @property
    def r(self):
        if self._is_rectangular:
            raise TypeError('No `r` value on a rectangular coordinate!')
        return self[0]

    @property
    def theta(self):
        if self._is_rectangular:
            raise TypeError('No `theta` value on a rectangular coordinate!')
        return self[1]

    def __repr__(self):
        if self._is_rectangular:
            return '{type.__name__}({self.x}, {self.y})'.format(type=type(self), self=self)
        return '{type.__name__}({self.r}, {self.theta}, False)'.format(type=type(self), self=self)

    def __abs__(self):
        if self._is_rectangular:
            return (self.x ** 2 + self.y ** 2) ** 0.5
        return self.r

    def to_polar(self):
        if self._is_rectangular:
            if self.x:
                theta = math.atan(self.y / self.x)
                if self.y < 0:
                    theta += math.pi
            elif self.y:
                if self.y > 0:
                    theta = math.tau / 4
                else:
                    theta = math.tau * 3 / 4
            else:
                theta = 0.0
            return type(self)(abs(self), theta, False)
        return +self

    def to_rect(self):
        if self._is_rectangular:
            return self
        return type(self)(self.r * math.cos(self.theta), self.r * math.sin(self.theta), True)

    def to_complex(self, complex_type=complex):
        return complex_type(*self.to_rect())

    def __complex__(self):
        return self.to_complex()

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            if other._is_rectangular and self._is_rectangular:
                return self.x == other.x and self.y == other.y
            elif not other._is_rectangular and not other._is_rectangular:
                return self.r == other.r and (self.theta % math.tau) == (other.theta % math.tau)
            return self.to_rect() == other.to_rect()
        return super(Coordinate, self).__eq__(other)

    @property
    def conjugate(self):
        return +type(self)(self[0], -self[1], self._is_rectangular)

    def __add__(self, other):
        if not isinstance(other, Coordinate):
            return NotImplemented
        rect_self = self.to_rect()
        other = other.to_rect()
        added = type(self)(rect_self.x + other.x, rect_self.y + other.y, True)
        if not self._is_rectangular:
            return added.to_polar()
        return added

    def __neg__(self):
        return +type(self)(-self[0], -self[1], self._is_rectangular)

    def __pos__(self):
        if self._is_rectangular:
            return type(self)(self.x, self.y, True)
        return type(self)(self.r, self.theta % math.tau, False)

    def __sub__(self, other):
        if not isinstance(other, Coordinate):
            return NotImplemented
        rect_self = self.to_rect()
        other = -other.to_rect()
        subtracted = type(self)(rect_self.x + other.x, rect_self.y + other.y, True)
        if not self._is_rectangular:
            return subtracted.to_polar()
        return subtracted

    def __mul__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        if self._is_rectangular:
            return type(self)(self.x * other, self.y * other, True)
        return +type(self)(self.r * other, self.theta, False)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        if self._is_rectangular:
            return type(self)(self.x / other, self.y / other, True)
        return +type(self)(self.r / other, self.theta, False)

    def rotate(self, angle):
        """Rotate anticlockwise by angle radians"""
        polar_self = self.to_polar()
        rotated = +type(self)(polar_self.r, polar_self.theta + angle)
        if self._is_rectangular:
            return rotated.to_rect()
        return rotated
