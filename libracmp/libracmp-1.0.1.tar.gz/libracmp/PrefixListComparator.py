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

import libracmp.ListComparator

import logging
logger = logging.getLogger('libracmp')


class PrefixListComparator(libracmp.ListComparator.ListComparator):
    """List item Comparator"""

    @property
    def result(self):
        """comparison property, performs the length indifferent comparison of list operands 
        from __init__ once computed result is cached, subsequent calls returns 
        cached value, object acts as immutable
        
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
                break  # Length indifference, comparing others on one side only skipped

        self._result = all(result_vector)
        if self._result:
            self._diff = None
        self.debug(self)
        return self._result
