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

"""
Filter objects are used to include, exclude, and transform data objects.
"""


class InvalidFilter(Exception):
    pass


class Filter(object):
    """Base filter class"""

    MATCHES = {
            'exact': lambda left, right: left == right,
            'substring': lambda inner, outer: str(inner) in str(outer),
            }

    def __init__(self, match='exact', what=None, data=None):
        """
        The *match* argument must be a callable object, or one of the following
        strings:

        * ``exact`` - an exact match (any type of object)
        * ``substring`` - a substring match (after conversion using
          :class:`str`)

        The *what* argument indicates which sort of element should be filtered.
        The object using the filter specifies the meaning of this field.

        The *data* argument contains the data the filter used when being
        applied.
        """

        if hasattr(match, '__call__'):
            self.match = match
        else:
            try:
                self.match = Filter.MATCHES[match]
            except KeyError as e:
                raise InvalidFilter(
                        'Invalid match %s: must be one of %s'
                        % (e.message, ', '.join(Filter.MATCHES.keys())))
        self.what = what
        self.data = data


class IncludeFilter(Filter):
    """
    Include matching elements. Provides an :meth:`include` method to test the
    given datum against the stored data using the :meth:`~Filter.match` method,
    as defined during initialization.
    """

    def include(self, datum):
        """Returns :data:`True` when the given ``datum`` should be included,
        or :data:`False` otherwise."""
        return self.match(self.data, datum)


class ExcludeFilter(Filter):
    """
    Exclude matching elements. Provides an :meth:`exclude` method to test the
    given datum against the stored data using the :meth:`~Filter.match` method,
    as defined during initialization.
    """

    def exclude(self, datum):
        """Returns :data:`True` when the given ``datum`` should be excluded,
        or :data:`False` otherwise."""
        return self.match(self.data, datum)


class TransformFilter(Filter):
    """
    Transform a matching element. In addition to the base :class:`Filter`
    attributes, a *transform* callable performs the transformation. Objects
    implementing transformations using this class specify the interface.
    """

    def __init__(self, match='exact', what=None, data=None, transform=None):
        """
        In addition to the arguments for :class:`Filter`, the *transform*
        argument is a callable object which is invoked when the filter is used.
        See: :meth:`transform`.
        """

        if not hasattr(transform, '__call__'):
            raise InvalidFilter('Transformation must be callable!')
        Filter.__init__(self, match=match, what=what, data=data)
        self.transform = transform
