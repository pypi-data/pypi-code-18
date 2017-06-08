# configstack/structures.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

import collections.abc
import functools
import os


__all__ = ['ConfigSection']


@functools.total_ordering
class ConfigSection(collections.abc.MutableMapping):
    """ A section of configuration options. """

    def __init__(self, name, options=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name

        if options is None:
            options = {}
        self._options = options

    def __repr__(self):
        text = "<{type} {name} options: [{options}]>".format(
                type=type(self).__name__,
                name=self.name,
                options=", ".join(sorted(list(self.options()))),
                )
        return text

    def __str__(self):
        text = "{type} {name} options: [{options}]".format(
                type=type(self).__name__,
                name=self.name,
                options=", ".join(sorted(list(self.options()))),
                )
        return text

    def __getitem__(self, key):
        return self._options[key]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __delitem__(self, key):
        del self._options[key]

    def __iter__(self):
        return iter(self._options)

    def __len__(self):
        return len(self._options)

    def options(self):
        """ Get a copy of the options collection in this section. """
        return dict(self._options)

    def _is_comparable(self, other):
        return isinstance(other, ConfigSection)

    def _comparison_tuple(self):
        option_set = {(name, value) for (name, value) in self.items()}
        comparison_tuple = (self.name, sorted(list(option_set)))
        return comparison_tuple

    def __eq__(self, other):
        if not self._is_comparable(other):
            return NotImplemented
        return self._comparison_tuple() == other._comparison_tuple()

    def __lt__(self, other):
        if not self._is_comparable(other):
            return NotImplemented
        return self._comparison_tuple() < other._comparison_tuple()


# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
