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

import AbstractComparator
import logging
logger = logging.getLogger('libracmp')


class RelaxedComparator(AbstractComparator.AbstractComparator):
    """Item comparator when None value is treated as wildcard, yielding True result"""

    @property
    def result(self):
        """comparison property, performs the comparison of operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        any None operand yields True result.
        None is treated as wildcard.
        
        :rtype: bool
        :return: comparison result, with None yielding True
        """
        if self._result is not None:
            return self._result
        if self.a_data is None or self.b_data is None:
            self._result = True
        else:
            self._result = self.a_data == self.b_data
        self.debug(self)
        return self._result

    def _compatible_types(self, a_item, b_item):
        """determine compatible types
        
        any None operand yields True result.
        None is treated as wildcard.
        
        :param a_item: first comparison operand
        :param b_item: second comparison operand
        :rtype: bool
        :return: type compatibility True if types match, with None yielding True
        """
        result = type(a_item) == type(b_item) or (a_item is None) or (b_item is None)
        self.debug('a_item=%s, b_item=%s -comp-> %s' % (a_item, b_item, result,))
        return result
