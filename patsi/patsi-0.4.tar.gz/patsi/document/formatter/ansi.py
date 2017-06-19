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
import six

from . import factory
from .. import tree
from .. import color
from .. import palette
from ...ansi import SGR


class AnsiFormatter(object):
    class Features(object):
        STANDARD    = 0     # Standard, only 8 colors supported
        BRIGHT_BOLD = 1     # Colors can be made bright by setting the bold flag
        BRIGHT      = 2     # Supports 9x codes for bright colors
        EXT_PALETTE = 256   # Supports 256-color palette (Code 38;5;*)
        RGB         = 4     # Supports 24 bit RGB colors (Code 38;2;r;g;b)
        ALL         = 0xFFF # All features are supported

        @classmethod
        def constants_dict(cls):
            if not hasattr(cls, "_constants_dict"):
                cls._constants_dict = {
                    name: value
                    for name, value in vars(cls).iteritems()
                    if name.isupper()
                }
            return cls._constants_dict

        @classmethod
        def feature_from_name(cls, name):
            return cls.constants_dict().get(name.strip().upper(), 0)

        def __init__(self, features=ALL):
            if type(features) is int:
                self.features = features
            elif isinstance(features, AnsiFormatter.Features):
                self.features = features.features
            else:
                if type(features) is str or type(features) is unicode:
                    features = features.split(", ")

                self.features = 0
                for feature in features:
                    if type(feature) is int:
                        self.features |= feature
                    else:
                        self.features |= self.feature_from_name(feature)

        def has_feature(self, feature):
            if type(feature) is str or type(feature) is unicode:
                feature = self.feature_from_name(feature)
            return (self.features & feature) == feature

    flat = True
    features = Features()

    def document(self, doc, output):
        self.layer(doc.flattened(), output)

    def layer(self, layer, output):
        if isinstance(layer, tree.Layer):
            for line in layer.text.splitlines(True):
                output.write(self.color(layer.color) + line)
        elif isinstance(layer, tree.FreeColorLayer):
            for y in six.moves.range(layer.height):
                prev_color = None
                for x in six.moves.range(layer.width):
                    char, col = layer.matrix.get((x, y), (" ", color.UnchangedColor))
                    if col is not color.UnchangedColor and col != prev_color:
                        prev_color = col
                        output.write(self.color(col))
                    output.write(char)
                output.write("\n")
        else:
            raise TypeError("Expected layer type")

    def color(self, col):
        return str(self._color_sgr(col))

    def _color_sgr(self, col):
        if col is None:
            ansi = SGR(SGR.ResetColor)
            self._bold = False
        elif isinstance(col, color.RgbColor):
            ansi = self._rgb_to_ansi(col)
        elif isinstance(col, color.IndexedColor):
            if len(col.palette) == 8:
                if getattr(col.palette, "bright", False):
                    ansi = self._16_to_ansi(col.index | 8)
                else:
                    ansi = self._8_to_ansi(col.index)
            elif len(col.palette) == 16:
                ansi = self._16_to_ansi(col.index)
            else:
                ansi = self._256_to_ansi(col)
        else:
            raise TypeError("Expected document color")

        if SGR.Bold in ansi.flags:
            self._bold = True
        elif getattr(self, "_bold", False):
            self._bold = False
            ansi.flags.append(SGR.reverse(SGR.Bold))
        return ansi

    def _rgb_to_ansi(self, col):
        if self.features.has_feature(AnsiFormatter.Features.RGB):
            return SGR(SGR.ColorRGB(col.r, col.g, col.b))
        if self.features.has_feature(AnsiFormatter.Features.EXT_PALETTE):
            return self._256_to_ansi(col.to_indexed(palette.colors256))
        return self._16_to_ansi(col.to_indexed(palette.colors16).index)

    def _8_to_ansi(self, index):
        return SGR(SGR.Color(index))

    def _16_to_ansi(self, index):
        bright = index > 7
        index = index & 7
        if not bright:
            return self._8_to_ansi(index)
        if self.features.has_feature(AnsiFormatter.Features.BRIGHT):
            return SGR(SGR.Color(index, False, True))
        if self.features.has_feature(AnsiFormatter.Features.BRIGHT_BOLD):
            return SGR(SGR.Color(index), SGR.Bold)
        return SGR(SGR.Color(index))

    def _256_to_ansi(self, col):
        if self.features.has_feature(AnsiFormatter.Features.EXT_PALETTE):
            return SGR(SGR.Color256(col.index))
        return self._rgb_to_ansi(col.rgb)

factory.register(AnsiFormatter(), "ansi")
