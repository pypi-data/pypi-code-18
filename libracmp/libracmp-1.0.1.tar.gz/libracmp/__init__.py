# Copyright 2017 Zdenek Kraus <zdenek.kraus@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import libracmp.StrictComparator
import libracmp.RelaxedComparator
import libracmp.TypeStrictComparator
import libracmp.IgnoreComparator
import libracmp.ListComparator
import libracmp.DictComparator

# Basic Strict equality using python ==
# ex: Value comparable values like int(1) == float(1.0) should be equals
MODE_STRICT = {
    'default': libracmp.StrictComparator.StrictComparator,
    'list': libracmp.ListComparator.ListComparator,
    'dict': libracmp.DictComparator.DictComparator,
}

# Basic relaxed equality, acts same as strict, with exception of None
# if one operand is None, then comparison is considered True
# missing Items dict.get() are treated as None and above applies
MODE_RELAXED = {
    'default': libracmp.RelaxedComparator.RelaxedComparator,
    'list': libracmp.ListComparator.ListComparator,
    'dict': libracmp.DictComparator.DictComparator,
}

# Type Strict equality first checks the compatible (equal) types
# ex: int vs floats are always false
MODE_TYPESTRICT = {
    'default': libracmp.TypeStrictComparator.TypeStrictComparator,
    'list': libracmp.ListComparator.ListComparator,
    'dict': libracmp.DictComparator.DictComparator,
}

# Ignore equality treats all operands comparison as True
# useful for filtering specific values
MODE_IGNORE = {
    'default': libracmp.IgnoreComparator.IgnoreComparator,
    'list': libracmp.ListComparator.ListComparator,
    'dict': libracmp.DictComparator.DictComparator,
}

# Default mode used is Basic Strict
MODE_DEFAULT = MODE_STRICT


def singleton(cls):
    """basic singleton decorator"""
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class All(object):
    """Wildcard key specifier used in filters
    
    Used as object in key, for applying sub-filter or comparator
    for all (default, not defined otherwise) values in such level.
    
    filter={All(): default_comparator, 'mykey': specific_comparator}
    for 'mykey', specific_comparator will be used,
    and for all others, default_comparator will be used. 
    """

    def __str__(self):
        return '<%all>'

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self