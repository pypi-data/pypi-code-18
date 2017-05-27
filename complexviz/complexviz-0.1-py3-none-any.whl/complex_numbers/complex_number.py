#!/usr/bin/env python

from math import sqrt, exp
from math import sin, cos, atan

class complex_number():
    """docstring for complex_number.

        Parameters:
        ----------

        x: int64, float64
            real component of the complex numbers

        y: int64, float64
            imaginary component of the complex number

        form: str (optional)
            format in which the complex number is to be saved

        Attributes:
        -------

        x: int64, float64
            real component of the complex numbers

        y: int64, float64
            imaginary component of the complex number

        format: str
            format in which the complex number is to be saved
    """
    def __init__(self, x=0, y=0, form="rectangular"):
        self.format = form
        self.x = x
        self.y = y

    def __repr__(self):
        """ Represents a complex number in `x + yi` format.

        Returns:
        -------
        str
            complex numner in `x + yi` format
        """
        if self.y > 0:
            msg = "{x} + {y}i".format(x=round(self.x, 2), y=round(self.y, 2))
        elif self.y < 0:
            msg = "{x} - {y}i".format(x=round(self.x, 2), y=-round(self.y, 2))
        elif self.y == 0:
            msg = "{x}".format(x=round(self.x, 2))
        return msg


    def __add__(self, other):
        """ Defines summation operation of two complex numbers.
            Overrides `+` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class, int, float

        Returns:
        -------

        complex_number class
            complex number summation self and other
        """
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
        elif isinstance(other, int) | isinstance(other, float):
            x = self.x + other
            y = self.y
        return self.__class__(x, y)

    def __sub__(self, other):
        """ Defines subtraction operation of two complex numbers.
            Overrides `-` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class

        Returns:
        -------

        complex_number class
            complex subtraction self and other
        """
        if isinstance(other, self.__class__):
            x = self.x - other.x
            y = self.y - other.y
        elif isinstance(other, int) | isinstance(other, float):
            x = self.x - other
            y = self.y
        return self.__class__(x, y)

    def __rsub__(self, other):
        """ Defines subtraction operation of two complex numbers.
            Overrides `-` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class

        Returns:
        -------

        complex_number class
            complex subtraction self and other
        """
        val = self.__sub__(other)
        val = val.__neg__()
        return val

    def __mul__(self, other):
        """ Defines multiplication operation of two complex numbers.
            Overrides `*` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class

        Returns:
        -------

        complex_number class
            complex multiplication self and other
        """
        if isinstance(other, self.__class__):
            x = self.x * other.x - self.y * other.y
            y = self.x * other.y + self.y * other.x
        elif isinstance(other, int) | isinstance(other, float):
            x = self.x * other
            y = self.y * other
        return self.__class__(x, y)

    def __truediv__(self, other):
        """ Defines division operation of two complex numbers.
            Overrides `/` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class

        Returns:
        -------

        complex_number class
            complex division self and other
        """
        if isinstance(other, self.__class__):
            denomenator = other.__mul__(other.conjugate())
            numerator = self.__mul__(other.conjugate())
            x = numerator.x / denomenator.x
            y = numerator.y / denomenator.x
        elif isinstance(other, int) | isinstance(other, float):
            other = self.__class__(other, 0)
            denomenator = other.__mul__(other.conjugate())
            numerator = self.__mul__(other.conjugate())
            x = numerator.x / denomenator.x
            y = numerator.y / denomenator.x
        return self.__class__(x, y)

    def __rtruediv__(self, other):
        """ Defines division operation of two complex numbers.
            Overrides `/` operatior.

        Parameters:
        ----------

        self: complex_number class
        other: complex_number class

        Returns:
        -------

        complex_number class
            complex division self and other
        """
        if isinstance(other, self.__class__):
            denomenator = self.__mul__(self.conjugate())
            numerator = other.__mul__(self.conjugate())
            x = numerator.x / denomenator.x
            y = numerator.y / denomenator.x
        elif isinstance(other, int) | isinstance(other, float):
            other = self.__class__(other, 0)
            denomenator = self.__mul__(self.conjugate())
            numerator = other.__mul__(self.conjugate())
            x = numerator.x / denomenator.x
            y = numerator.y / denomenator.x
        return self.__class__(x, y)

    __rmul__ = __mul__
    __radd__ = __add__

    def conjugate(self):
        """ Returns conjugate of a complex number

        Returns:
        -------

        complex_number class
            conjugate of a complex number
        """
        return self.__class__(self.x, -self.y)

    def __abs__(self):
        """ Returns absolute value of a complex number

        Returns:
        -------

        complex_number class
            absolute value of a complex number
        """
        return sqrt(self.x**2 + self.y**2)

    def __neg__(self):
        return self.__mul__(-1)

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __pow__(self, power):
        pass

    def argument(self):
        return atan(self.y/self.y)

    def to_polar(self):
        if self.format is not "polar":
            x = self.__abs__()
            y = self.argument()
            self.x = x
            self.y = y
            self.format = "polar"
