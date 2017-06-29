from __future__ import division

import numbers
import cmath
import math

__all__ = (
    'TypedComplex', 'IntComplex', 'DecimalComplex', 'BoolComplex',
    'FloatComplex', 'FractionComplex'
)


class TypedComplex(numbers.Complex):
    """A complex number with customisable types for its real and imaginary parts"""
    type = None

    def __new__(cls, re, im=None):
        if im is None:
            if not isinstance(re, numbers.Complex):
                raise TypeError('Must give a complex number or two reals')
            re, im = re.real, re.imag
        self = super(TypedComplex, cls).__new__(cls)
        super(TypedComplex, self).__init__()
        self._real = self.type(re)
        self._imag = self.type(im)
        return self

    def __abs__(self):
        return (self.imag ** 2 + self.real ** 2) ** 0.5

    def __add__(self, other):
        if isinstance(other, numbers.Complex):
            return type(self)(self.real + other.real, self.imag + other.imag)
        if isinstance(other, numbers.Real):
            return type(self)(self.real + other, self.imag)
        return NotImplemented

    def __complex__(self):
        return complex(self.real, self.imag)

    def __eq__(self, other):
        if isinstance(other, numbers.Complex):
            return self.imag == other.imag and self.real == other.real
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, numbers.Complex):
            return self.imag != other.imag or self.real != other.real
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return type(self)(self.real * other, self.imag * other)
        if isinstance(other, numbers.Complex):
            return type(self)(self.real * other.real - self.imag * other.imag, self.real * other.imag + self.imag * other.real)
        return NotImplemented

    def __neg__(self):
        return type(self)(-self.real, -self.imag)

    def __pos__(self):
        return type(self)(self)

    def __pow__(self, other):
        i = type(self)(0, 1)
        one = type(self)(1, 0)
        if isinstance(other, numbers.Real):
            r = abs(self)
            theta = cmath.phase(self)
            return (r ** other) * (one * math.cos(other * theta) + i * (math.sin(other * theta)))
        elif isinstance(other, numbers.Complex):
            r = abs(self)
            theta = cmath.phase(self)
            return (r ** other) * (one * cmath.cos(other * theta) + i * (cmath.sin(other * theta)))
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rpow__(self, other):
        if isinstance(other, numbers.Complex):
            a = ((other ** 2) ** (self.real / 2)) * math.e ** (-self.imag * cmath.phase(other))
            b = 0.5 * self.imag * math.log(other ** 2) + self.real * cmath.phase(other)
            return type(self)(1, 0) * (a * math.cos(b)) + type(self)(0, 1) * (a * math.sin(b))
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Complex):
            return type(self).__truediv__(other, self)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return type(self)(self.real / other, self.imag / other)
        if isinstance(other, numbers.Complex):
            denom = other.real ** 2 + other.imag ** 2
            return type(self)((self.real * other.real + self.imag * other.imag) / denom, (self.imag * other.real - self.real * other.imag) / denom)
        return NotImplemented

    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    @property
    def conjugate(self):
        return type(self)(self.real, -self.imag)

    @property
    def imag(self):
        return self._imag

    @property
    def real(self):
        return self._real

    def __repr__(self):
        return '{type.__name__}({self.real!r}, {self.imag!r})'.format(self=self, type=type(self))

    def __hash__(self):
        as_complex = complex(self)
        if as_complex == self:
            return hash(as_complex)
        try:
            return hash((self.real, self.imag))
        except TypeError:
            # Unhashable real number type
            return hash(as_complex)

    def __floor__(self):
        return type(self)(math.floor(self.real), math.floor(self.imag))

    def __ceil__(self):
        return type(self)(math.ceil(self.real), math.ceil(self.imag))

    def __round__(self, n=None):
        return type(self)(round(self.real, n), round(self.imag, n))

    def __bool__(self):
        return bool(self.real or self.imag)

    def __hex__(self):
        try:
            return '(0x{self.real:x}+0x{self.imag:x}j)'.format(self=self)
        except TypeError:
            return NotImplemented

    def __floordiv__(self, other):
        div = self.__truediv__(other)
        if div is NotImplemented:
            return NotImplemented
        return div.__floor__()

    def __rfloordiv__(self, other):
        div = self.__rtruediv__(other)
        if div is NotImplemented:
            return NotImplemented
        return div.__floor__()

    def __oct__(self):
        try:
            return '(0o{self.real:o}+0o{self.imag:o}j)'.format(self=self)
        except TypeError:
            return NotImplemented

    def __reversed__(self):
        return type(self)(self.imag, self.real)

    def __invert__(self):
        return self.conjugate

    def __mod__(self, other):
        if isinstance(other, numbers.Complex):
            return self + other * (-self / other).__ceil__()
        return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, numbers.Complex):
            return other + self * type(self).__ceil__(-other / self)
        return NotImplemented

    def equals(self, other, tolerance=1e-15):
        return abs(self - other) <= tolerance


class IntComplex(TypedComplex):
    type = int


class DecimalComplex(TypedComplex):
    from decimal import Decimal as type


class BoolComplex(TypedComplex):
    type = bool


class FloatComplex(TypedComplex):
    type = float
    # Note: Should be equivalent to builtin :func:`complex`

class FractionComplex(TypedComplex):
    from fractions import Fraction as type
