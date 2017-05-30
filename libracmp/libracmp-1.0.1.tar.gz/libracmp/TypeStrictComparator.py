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

import libracmp.AbstractComparator
import logging
logger = logging.getLogger('libracmp')


class TypeStrictComparator(libracmp.AbstractComparator.AbstractComparator):
    """Item comparator checking for type match before comparison, non-matching types yields False result"""
    @property
    def result(self):
        """comparison property, performs the comparison of operands from __init__
        once computed result is cached, subsequent calls returns cached value, object acts as immutable
        
        first types are checked. Non-matching types yields False results.
        Then regular comparison is performed
        
        :rtype: bool
        :return: comparison result
        """
        if self._result is not None:
            return self._result
        if not self._compatible_types(self.a_data, self.b_data):
            self._result = False
        else:
            self._result = super(TypeStrictComparator, self).result
        return self._result
