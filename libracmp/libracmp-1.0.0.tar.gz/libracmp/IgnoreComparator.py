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


class IgnoreComparator(AbstractComparator.AbstractComparator):
    """Item Comparator for ignoring particular comparison results"""

    @property
    def result(self):
        """comparison property, performs the comparison of operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        Any values are treated as equals.
        
        :rtype: bool
        :return: always returns True
        """
        if self._result is not None:
            return self._result
        self._result = True
        self.debug(self)
        return self._result

    def _compatible_types(self, a_item, b_item):
        """determine compatible types
        
        All values are treated as equal types.
                
        :param a_item: first comparison operand
        :param b_item: second comparison operand
        :rtype: bool
        :return: always returns True
        """
        result = True
        self.debug('a_item=%s, b_item=%s -comp-> %s' % (a_item, b_item, result,))
        return result
