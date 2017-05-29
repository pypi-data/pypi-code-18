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

from unittest import TestCase
from libracmp.ListComparator import ListComparator


class TestResultListComparator(TestCase):

    def test_result_listEmpty_listEmpty_eq(self):
        a = []
        b = []
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listEmpty_listStra_neq(self):
        a = []
        b = ['a']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_listEmpty_neq(self):
        a = ['a']
        b = []
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_listStraa_neq(self):
        a = ['a']
        b = ['a', 'a']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStraa_listStra_neq(self):
        a = ['a', 'a']
        b = ['a']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStrabcde1_listStrabcde1_eq(self):
        a = ['a', 'b', 'c', 'd', 'e', '1']
        b = ['a', 'b', 'c', 'd', 'e', '1']
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listStrabcde1_listStrabcde2_neq(self):
        a = ['a', 'b', 'c', 'd', 'e', '1']
        b = ['a', 'b', 'c', 'd', 'e', '2']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStrabcde1_listStrab9cde1_neq(self):
        a = ['a', 'b', 'c', 'd', 'e', '1']
        b = ['a', 'b', 9, 'c', 'd', 'e', '1']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistab_listlistab_eq(self):
        a = [['a'], ['b']]
        b = [['a'], ['b']]
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistab_listlistac_neq(self):
        a = [['a'], ['b']]
        b = [['a'], ['c']]
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistlistab_listlistlistab_eq(self):
        a = [['a'], [['b']]]
        b = [['a'], [['b']]]
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistlistab_listlistlistac_neq(self):
        a = [['a'], [['b']]]
        b = [['a'], [['c']]]
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistlistab_c_listlistlistab_c_eq(self):
        a = [['a'], [['b']], 'c']
        b = [['a'], [['b']], 'c']
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistlistab_c_listlistlistab_d_neq(self):
        a = [['a'], [['b']], 'c']
        b = [['a'], [['b']], 'd']
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_mlistab_mlistab_eq(self):
        a = [[[[[['a', 'b']]]]]]
        b = [[[[[['a', 'b']]]]]]
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_mlistab_mlistac_neq(self):
        a = [[[[[['a', 'b']]]]]]
        b = [[[[[['a', 'c']]]]]]
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_mlistab_mlistablistc_neq(self):
        a = [[[[[['a', 'b']]]]]]
        b = [[[[[['a', 'b', ['c']]]]]]]
        comp = ListComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listvalues_listvalues_eq(self):
        a = [None, True, False, 0, 1, -1, 0.0, 1.0, -1.0, 'a', u'b']
        b = [None, True, False, 0, 1, -1, 0.0, 1.0, -1.0, 'a', u'b']
        comp = ListComparator(a, b)
        self.assertTrue(comp.result)
