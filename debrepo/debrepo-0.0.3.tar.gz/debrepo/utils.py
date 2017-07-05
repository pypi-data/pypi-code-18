# Copyright (c) 2016 Andrew Hills
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

import string


class PluralFormatter(string.Formatter):
    """Formatter syntax: ``{key|unit}``, ``{key~sep}``

    The *key* is the index of the argument or the key of the keyword argument
    to interpret and interpolate. The value must be an integer.

    The *unit* can be "base(suffix)" or "either/or", e.g.:

    * antenna(e)
    * goose/geese
    * fox(es)

    If unit is preceded by a \*, take ``len(value)`` instead of value as the
    count (i.e., ``{key|*item(s)}`` will count the values at *key* instead of
    interpreting the value at *key* as the count directly).

    In the second form, *sep* is a string with which to join the list indicated
    by *key* (and the value must be a valid argument to :func:`string.join`).

    Examples:

    .. code-block:: python

       >>> geese = [ 'goose1', 'goose2' ]
       >>> FMT.format('Your geese are {0~ & }', geese)
       'Your geese are goose1 & goose2'
       >>> FMT.format('You still have {0|goose/geese}', len(geese))
       'You still have 2 geese'
       >>> geese = [ 'goose1' ]
       >>> FMT.format('You still have {geese|*goose/geese}', geese=geese)
       'You still have 1 goose'
    """

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return args[key]
        if key in kwargs:
            return kwargs[key]
        if '|' in key:
            compute_len = False
            key, rest = key.split('|', 1)
            if rest.startswith('*'):
                compute_len = True
                rest = rest[1:]
            if '/' in rest:
                words = rest.split('/', 1)
            elif '(' in rest and rest.endswith(')'):
                word, suffix = rest.split('(')
                words = [word, word + suffix.rstrip(')')]
            if key in kwargs:
                value = kwargs[key]
            else:
                try:
                    index = int(key)
                except ValueError:
                    raise KeyError(key)
                value = args[index]
            if compute_len:
                value = len(value)
            if not isinstance(value, int):
                raise TypeError('Plurality only applies to numbers!')
            return '{0} {1}'.format(value, words[0 if value == 1 else 1])
        elif '~' in key:
            key, sep = key.split('~', 1)
            if key in kwargs:
                values = kwargs[key]
            else:
                try:
                    index = int(key)
                except ValueError:
                    raise KeyError(key)
                values = args[index]
            return sep.join(values)
        else:
            raise KeyError(key)

#: Instance of :class:`PluralFormatter` exported for convenience
FMT = PluralFormatter()
