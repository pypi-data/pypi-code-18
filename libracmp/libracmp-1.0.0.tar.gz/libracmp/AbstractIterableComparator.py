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

import libracmp.exceptions
import libracmp.AbstractComparator

import logging
logger = logging.getLogger('libracmp')


class AbstractIterableComparator(libracmp.AbstractComparator.AbstractComparator):
    """Abstract object for Iterable (list) objects Comparator classes in libracmp module"""

    @property
    def result(self):
        """comparison property, performs the comparison of list operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        comparison is done as iteration of iterable items of operands.
        subsequent comparators are used on particular item pairs, -> recursively
        
        if lengths differs, comparison continues, so diff is computed completely.
        
        diff is actually computed in result for efficiency.
        
        :rtype: bool
        :return: comparison result
        """
        if self._result is not None:
            return self._result
        self._diff = []
        length = max(len(self.a_data), len(self.b_data))
        self.debug('length=%s' % (length,))
        result_vector = []
        for i_indx in xrange(length):
            a_item = None
            b_item = None
            length_error = False
            try:
                a_item = self.a_data[i_indx]
            except IndexError:
                length_error = True
            try:
                b_item = self.b_data[i_indx]
            except IndexError:
                length_error = True
            if not length_error:
                self.debug('i_indx=%s, a_item=%s, b_item=%s' % (i_indx, a_item, b_item,))
                comparator = self._compare_next(a_item, b_item, i_indx)()
                result_vector.append(comparator.result)
                if comparator.diff is not None:
                    self._diff.append(comparator.diff)
            else:
                result_vector.append(False)
                self._diff.append((a_item, b_item))

        self._result = all(result_vector)
        if self._result:
            self._diff = None
        self.debug(self)
        return self._result

    @property
    def diff(self):
        """provides comparison differences if applicable
        diff is computed (by result) and cached, subsequent calls return cached value, object acts as immutable
        :rtype: None, set, list, dict
        :return: comparison differences
        """
        if self._diff is not None:
            return self._diff
        _ = self.result
        return self._diff

    def _compare_next(self, a_next, b_next, i_key):
        """internal subsequent compare of selected item pair
        
        :param a_next: first operand to compare
        :param b_next: second operand to compare
        :type i_key: int, str
        :param i_key: context key / index used for selecting specific filters
        :rtype: lambda
        :return: function that spawn instance of subsequent comparator
        """
        self.debug('mode=%s' % self.mode)
        comparator_next = None
        filters_next = self._select_filters(i_key)

        if (filters_next
                and not isinstance(filters_next, dict)
                and issubclass(filters_next, libracmp.AbstractComparator.AbstractComparator)):
            comparator_next = filters_next
            filters_next = None
        elif isinstance(a_next, dict) and isinstance(b_next, dict):
            comparator_next = self.mode.get('dict')
        elif isinstance(a_next, (list, tuple)) and isinstance(b_next, (list, tuple)):
            comparator_next = self.mode.get('list')

        # getting default
        if comparator_next is None:
            comparator_next = self.mode.get('default')
            if not comparator_next or not issubclass(comparator_next, libracmp.AbstractComparator.AbstractComparator):
                raise libracmp.exceptions.CannotCompareError(
                    'Cannot determine any suitable comparator to use, for current mode \"%s\"' % (self.mode,)
                )
        self.debug('comparator_next=%s' % (comparator_next,))

        return lambda: comparator_next(a_next, b_next, filters_next, self.aux, self.mode, self.depth+1)

    def _select_filters(self, i_key):
        """internal filter selector, used for subsequent comparison
        
        select specific comparator or subfilter, depending on original filter.
        if there is no filter available for specific key, default is selected.
        and if there is no default, None is returned.
        
        If no key is specified, complete filter is returned.
        If no original filter exists Non is returned.
        
        :param i_key: context key, to select filter
        :rtype: dict, libracmp.AbstractIterator.AbstractIterator, None
        :return: selected filter, else default, otherwise None
        """
        if i_key is None or self.filters is None:
            return self.filters
        # select particular filters
        tmp = self.filters.get(i_key)
        if tmp is not None:
            result = tmp
        # select defaults
        else:
            result = self.filters.get(libracmp.All())
        self.debug('_select_filter=%s' % (result,))
        return result
