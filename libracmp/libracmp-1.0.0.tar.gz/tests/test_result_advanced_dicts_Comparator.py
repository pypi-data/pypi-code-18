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
from libracmp.Comparator import Comparator


class TestResultComparator(TestCase):

    def test_result_listEmpty_listEmpty_eq(self):
        a = {}
        b = {}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listEmpty_listStra_neq(self):
        a = {}
        b = {'a': 'a'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_listEmpty_neq(self):
        a = {'a': 'a'}
        b = {}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_listStraa_neq(self):
        a = {'a': 'a'}
        b = {'a': 'a', 'b': 'a'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStraa_listStra_neq(self):
        a = {'a': 'a', 'b': 'a'}
        b = {'a': 'a'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStrabcde1_listStrabcde1_eq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listStrabcde1_listStrabcde2_neq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '2'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStrabcde1_listStrab9cde1_neq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 9: 9, 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistab_listlistab_eq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': 'b'}}
        b = {'a': {'a': 'a'}, 'b': {'a': 'b'}}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistab_listlistac_neq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': 'b'}}
        b = {'a': {'a': 'a'}, 'b': {'a': 'c'}}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistlistab_listlistlistab_eq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}}
        b = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistlistab_listlistlistac_neq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}}
        b = {'a': {'a': 'a'}, 'b': {'a': {'a': 'c'}}}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listlistlistab_c_listlistlistab_c_eq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}, 'c': 'c'}
        b = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}, 'c': 'c'}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listlistlistab_c_listlistlistab_d_neq(self):
        a = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}, 'c': 'c'}
        b = {'a': {'a': 'a'}, 'b': {'a': {'a': 'b'}}, 'c': 'd'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_mlistab_mlistab_eq(self):
        a = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'b'}}}}}}
        b = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'b'}}}}}}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_mlistab_mlistac_neq(self):
        a = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'b'}}}}}}
        b = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'c'}}}}}}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_mlistab_mlistablistc_neq(self):
        a = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'b'}}}}}}
        b = {'a': {'a': {'a': {'a': {'a': {'a': 'a', 'b': 'b', 'c': {'a': 'c'}}}}}}}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listvalues_listvalues_eq(self):
        a = {'a': None, 'b': True, 'c': False, 'd': 0, 'e': 1, 'f': -1,
             'g': 0.0, 'h': 1.0, 'i': -1.0, 'j': 'a', 'k': u'b'}
        b = {'a': None, 'b': True, 'c': False, 'd': 0, 'e': 1, 'f': -1,
             'g': 0.0, 'h': 1.0, 'i': -1.0, 'j': 'a', 'k': u'b'}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)
