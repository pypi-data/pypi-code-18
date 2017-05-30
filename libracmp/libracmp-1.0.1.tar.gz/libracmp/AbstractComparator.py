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


import libracmp
import logging

logger = logging.getLogger('libracmp')


class AbstractComparator(object):
    """Abstract object for Comparator classes in libracmp module"""

    def __init__(self, a_data, b_data, filters=None, aux=None, mode=None, depth=0):
        """operands are stored in class, to be then compared by .result property use
        
        filters specify exceptional care of specific keys/index (applicable with iterable comparators)
        
        aux is not currently used
        
        mode specifies default selection of comparators for values (applicable with iterable comparators)
        mode has contain 'default', 'list', 'dict' keys with comparator classes to be used for that occasion
        
        depth is internal depth counter used for indented logging, and debugging
        
        :param a_data: first operand to compare
        :param b_data: second operand to compare
        :type filters: dict
        :param filters: comparison filter
        :param aux: Auxilliary data
        :type mode: dict
        :param mode: Comparison mode for selecting comparators based on types
            dict must contain 3 keys 'default', 'list', 'dict' with selected comparator classes
        :param depth: internal depth modifier
        """
        self.a_data = a_data
        self.b_data = b_data
        self.filters = filters
        self.aux = aux
        self.mode = mode or libracmp.MODE_DEFAULT
        self._result = None
        self._diff = None
        self.depth = depth

    @property
    def result(self):
        """comparison property, performs the comparison of operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        :rtype: bool
        :return: comparison result
        """
        if self._result is not None:
            return self._result
        self._result = self.a_data == self.b_data
        self.debug(self)
        return self._result

    @property
    def diff(self):
        """provides comparison differences if applicable
        diff is computed and cached, subsequent calls return cached value, object acts as immutable
        :rtype: None, set, list, dict
        :return: comparison differences
        """
        if self._diff is not None:
            return self._diff
        self._diff = None
        if not self.result:
            self._diff = (self.a_data, self.b_data,)
        return self._diff

    def _compatible_types(self, a_item, b_item):
        """determine compatible types
        result might actually depend on used comparator
        
        :param a_item: first comparison operand
        :param b_item: second comparison operand
        :rtype: bool
        :return: type compatibility True if types match
        """
        result = type(a_item) == type(b_item)
        self.debug('a_item=%s, b_item=%s -comp-> %s' % (a_item, b_item, result,))
        return result

    def __str__(self):
        tmp = ("%s(A=%s, B=%s, filters=%s, aux=%s, mode=%s, depth=%s) -> %s diff=%s"
               % (self.__class__.__name__, repr(self.a_data), repr(self.b_data),
                  self.filters, self.aux, self.mode, self.depth, self.result, self.diff))
        return tmp

    def debug(self, msg):
        logger.debug("%s> %s" % (self.depth, msg))
