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


class StringCastComparator(AbstractComparator.AbstractComparator):
    """Item comparator performing string cast before comparison"""

    def __init__(self, a_data, b_data, filters=None, aux=None, mode=None, depth=0):
        """comparison operands are casted to string to perform a string compare
        
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
        super(StringCastComparator, self).__init__(a_data, b_data, filters, aux, mode, depth)
        self.a_data = str(a_data)
        self.b_data = str(b_data)
