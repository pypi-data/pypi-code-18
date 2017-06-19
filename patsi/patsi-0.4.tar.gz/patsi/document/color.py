#
# Copyright (C) 2016-2017 Mattia Basaglia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from math import sqrt, floor


class IndexedColor(object):
    """
    Color within a palette
    """
    def __init__(self, color, palette):
        if type(color) is str:
            self.index = palette.find_index(color)
        else:
            self.index = color

        self.palette = palette

    @property
    def rgb_tuple(self):
        """
        Returns a tuple with the rgb components
        """
        return self.palette.rgb_tuple(self.index)

    @property
    def rgb(self):
        """
        Returns a RgbColor object corresponding to this color
        """
        return self.palette.rgb(self.index)

    @property
    def name(self):
        """
        Color name as from the palette
        """
        return self.palette.name(self.index)

    def __eq__(self, oth):
        """
        Compares the rgb tuple of two colors to check whether they are the same
        """
        return self.rgb_tuple == RgbColor._color_tuple(oth)

    def __ne__(self, oth):
        """
        Compares the rgb tuple of two colors to check whether they are the same
        """
        return not (self == oth)

    def __hash__(self):
        return hash((IndexedColor, self.index, self.palette))


class RgbColor(object):
    """
    24 Bit RGB color
    """
    def __init__(self, r, g, b, name=None):
        self.r = r
        self.g = g
        self.b = b
        self._name = name

    @property
    def rgb_tuple(self):
        """
        Returns a tuple with the rgb components
        """
        return (self.r, self.g, self.b)

    @property
    def rgb(self):
        """
        Returns a RgbColor object corresponding to this color
        """
        return self

    @property
    def name(self):
        """
        Color name (if set) otherwise the hex string
        """
        return self._name if self._name is not None else self.hex()

    @name.setter
    def name(self, name):
        """
        Sets the color name to a specific string
        """
        self._name = name

    @name.deleter
    def name(self):
        """
        Resets the name to the default (which is the same as hex)
        """
        self._name = None

    def __eq__(self, oth):
        """
        Compares the rgb tuple of two colors to check whether they are the same
        """
        return self.rgb_tuple == RgbColor._color_tuple(oth)

    def __ne__(self, oth):

        """
        Compares the rgb tuple of two colors to check whether they are the same
        """
        return not (self == oth)

    def copy(self):
        """
        Returns a deep copy of this object
        """
        return RgbColor(self.r, self.g, self.b, self.name)

    def hex(self):
        """
        Hex string for this color
        """
        return '#%02x%02x%02x' % self.rgb_tuple

    @staticmethod
    def _color_tuple(obj):
        """
        Returns a rgb tuple for comaring color-like objects
        """
        if obj is None:
            return tuple()
        if type(obj) is tuple and len(obj) == 3:
            return obj
        return obj.rgb_tuple

    def __hash__(self):
        return hash((RgbColor, self.rgb_tuple))

    def rgb_float(self):
        """
        Returns normalized RGB components
        """
        return (
            self.r / 255.0,
            self.g / 255.0,
            self.b / 255.0,
        )

    def _xyz(self):
        """
        Converts the color into XYZ coordinates
        """
        redf, greenf, bluef = self.rgb_float()

        def conv(v):
            return ((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92
        redf = conv(redf) * 100
        greenf = conv(greenf) * 100
        bluef = conv(bluef) * 100

        X = redf * 0.4124 + greenf * 0.3576 + bluef * 0.1805
        Y = redf * 0.2126 + greenf * 0.7152 + bluef * 0.0722
        Z = redf * 0.0193 + greenf * 0.1192 + bluef * 0.9505

        return (X, Y, Z)

    def lab(self):
        """
        Converts the color into L*a*b* coordinates
        """
        X, Y, Z = self._xyz()

        ref_X =  95.047
        ref_Y = 100.000
        ref_Z = 108.883

        x = X / ref_X
        y = Y / ref_Y
        z = Z / ref_Z

        def conv(v):
            return v ** (1.0 / 3) if v > 0.008856 else (7.787 * v) + (16.0 / 116)
        x = conv(x)
        y = conv(y)
        z = conv(z)

        L = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)

        def to_int(v):
            return int(round(v))
        return (to_int(L), to_int(a), to_int(b))

    def distance(self, other):
        """
        Evaluates the Delta-E distance between two RGB colors
        """
        return sqrt(sum(map(lambda a: (a[0] - a[1]) ** 2, zip(self.lab(), other.lab()))))

    def to_indexed(self, palette):
        """
        Returns the monst similar color from the palette
        """
        if not palette:
            raise ValueError("Cannot convert to an indexed color with an empty palette")

        min_distance = self.distance(palette.rgb(0))
        min_index = 0
        for index, color in enumerate(palette.colors):
            distance = self.distance(RgbColor(*color))
            if distance < min_distance:
                min_distance = distance
                min_index = index

        return IndexedColor(min_index, min_distance)

    @classmethod
    def from_hsv(cls, h, s, v):
        """
        Coverts from HSV components
        Each component shall be in [0, 1]
        """
        if h < 0:
            h = 0
        elif h > 1:
            h %= 1
        s = min(max(s, 0), 1)
        v = min(max(v, 0), 1)

        h *= 6
        c = v * s
        m = v - c

        h1 = floor(h)
        f = h - h1
        n = v - c * f
        k = v - c * (1 - f)

        v = int(round(v * 255))
        m = int(round(m * 255))
        n = int(round(n * 255))
        k = int(round(k * 255))

        if h1 == 0:
            return cls(v, k, m)
        elif h1 == 1:
            return cls(n, v, m)
        elif h1 == 2:
            return cls(m, v, k)
        elif h1 == 3:
            return cls(m, n, v)
        elif h1 == 4:
            return cls(k, m, v)
        elif h1 == 5:
            return cls(v, m, n)
        else: # h1 == 6
            return cls(v, k, m)

    def hsv(self):
        """
        Returns a tuple with normalized HSV components
        """
        r, g, b = self.rgb_float()
        if r == g == b:
            cmax = r
            h = 0
            delta = 0
        else:
            cmax = max(r, g, b)
            cmin = min(r, g, b)
            delta = cmax - cmin

            if cmax == r:
                h = ((g - b) / delta) % 6
            elif cmax == g:
                h = (b - r) / delta + 2
            else: # cmax == b
                h = (r - g) / delta + 4

        h /= 6
        s = delta / cmax if cmax > 0 else 0
        v = cmax

        return (h, s, v)


class UnchangedColorType(object):
    """
    Dummy class for the UnchangedColor constant
    """
    pass


UnchangedColor = UnchangedColorType()
