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

import libracmp.AbstractIterableComparator

import logging
logger = logging.getLogger('libracmp')


class DictComparator(libracmp.AbstractIterableComparator.AbstractIterableComparator):
    """dict objects Comparator"""

    @property
    def result(self):
        """comparison property, performs the comparison of dict operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        comparison is done as iteration of iterable items of operands by keys.
        subsequent comparators are used on particular item pairs, -> recursively
        
        if key is missing, None is used as value, then the result depends on next comparator type (mode/filters)
        
        diff is actually computed in result for efficiency.
        
        :rtype: bool
        :return: comparison result
        """
        if self._result is not None:
            return self._result
        self._diff = {}
        keys = set(self.a_data.keys() + self.b_data.keys())
        self.debug('keys=%s' % (keys,))
        result_vector = []
        for i_key in keys:
            a_item = self.a_data.get(i_key)
            b_item = self.b_data.get(i_key)
            self.debug('i_key=%s, a_item=%s, b_item=%s' % (i_key, a_item, b_item,))
            comparator = self._compare_next(a_item, b_item, i_key)()
            result_vector.append(comparator.result)
            if comparator.diff is not None:
                self._diff[i_key] = comparator.diff

        self._result = all(result_vector)
        if self._result:
            self._diff = None
        self.debug(self)
        return self._result
