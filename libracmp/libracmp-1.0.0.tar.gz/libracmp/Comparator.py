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


class Comparator(libracmp.AbstractIterableComparator.AbstractIterableComparator):
    """omni objects Comparator
    does not compare itself, but can be used for various operand types.
    Acts as entry comparator to be used by default.
    """

    @property
    def result(self):
        """comparison property, performs the comparison of dict operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        comparison is done by subsequent specific type comparator.
        
        :rtype: bool
        :return: comparison result
        """
        if self._result is not None:
            return self._result
        self._diff = None
        comparator = self._compare_next(self.a_data, self.b_data, None)()
        self._result = comparator.result
        if comparator.diff is not None:
            self._diff = comparator.diff

        if self._result:
            self._diff = None
        self.debug(self)
        return self._result
