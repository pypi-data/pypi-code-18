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
import libracmp
from libracmp.Comparator import Comparator
from libracmp.StrictComparator import StrictComparator
from libracmp.RelaxedComparator import RelaxedComparator
from libracmp.IgnoreComparator import IgnoreComparator

import libracmp.AbstractIterableComparator


class TestResultFiltersComparator(TestCase):

    def test_result_filter_list_all_relaxed_eq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['a', 'b', 'c', 'd', None]
        filters = {libracmp.All(): RelaxedComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_list_all_strict_neq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['a', 'b', 'c', 'd', None]
        filters = {libracmp.All(): StrictComparator}
        comp = Comparator(a, b, filters=filters, mode=libracmp.MODE_IGNORE)
        self.assertFalse(comp.result)

    def test_result_filter_list_index0_strict_neq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['x', 'b', 'c', 'd', None]
        filters = {0: StrictComparator}
        comp = Comparator(a, b, filters=filters, mode=libracmp.MODE_IGNORE)
        self.assertFalse(comp.result)

    def test_result_filter_list_index1_strict_neq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['a', 'x', 'c', 'd', None]
        filters = {1: StrictComparator}
        comp = Comparator(a, b, filters=filters, mode=libracmp.MODE_IGNORE)
        self.assertFalse(comp.result)

    def test_result_filter_list_index0_ignore_eq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['x', 'b', 'c', 'd', 'e']
        filters = {0: IgnoreComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_list_index1_ignore_eq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['a', 'x', 'c', 'd', 'e']
        filters = {1: IgnoreComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_list_multiple_eq(self):
        a = ['a', 'b', 'c', 'd', 'e']
        b = ['a', 'x', 'x', 'd', None]
        filters = {1: IgnoreComparator, 2: IgnoreComparator, 4: RelaxedComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_list_multilevel_eq(self):
        a = ['a', ['b'], ['c'], 'd', 'e']
        b = ['a', ['x'], ['c'], 'd', 'e']
        filters = {1: {libracmp.All(): IgnoreComparator}}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_list_multilevel_multiple_eq(self):
        a = ['a', ['b'], ['c'], 'd', 'e']
        b = ['a', ['x'], ['y'], 'd', 'e']
        filters = {1: {libracmp.All(): IgnoreComparator}, 2: {0: IgnoreComparator}}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_dict_all_relaxed_eq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': None, '1': '1'}
        filters = {libracmp.All(): RelaxedComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_dict_keye_relaxed_eq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': None, '1': '1'}
        filters = {'e': RelaxedComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_dict_keye_strict_neq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': None, '1': '1'}
        filters = {'e': StrictComparator}
        comp = Comparator(a, b, filters=filters, mode=libracmp.MODE_IGNORE)
        self.assertFalse(comp.result)

    def test_result_filter_dict_multiple_eq(self):
        a = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': 'x', 'c': 'y', 'd': 'd', 'e': None, '1': '1'}
        filters = {'b': IgnoreComparator, 'c': IgnoreComparator, 'e': RelaxedComparator}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_dict_multilevel_eq(self):
        a = {'a': 'a', 'b': {'b': 'b'}, 'c': {'c': 'c'}, 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': {'b': 'x'}, 'c': {'c': 'c'}, 'd': 'd', 'e': 'e', '1': '1'}
        filters = {'b': {libracmp.All(): IgnoreComparator}}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_dict_multilevel_multiple_eq(self):
        a = {'a': 'a', 'b': {'b': 'b'}, 'c': {'c': 'c'}, 'd': 'd', 'e': 'e', '1': '1'}
        b = {'a': 'a', 'b': {'b': 'x'}, 'c': {'c': 'y'}, 'd': 'd', 'e': 'e', '1': '1'}
        filters = {'b': {libracmp.All(): IgnoreComparator}, 'c': {'c': IgnoreComparator}}
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)

    def test_result_filter_listdict_multilevel_eq(self):
        a = [
            {'a': 'a11', 'b': 'b1', 'p': {'x': 'x'}},
            {'a': 'a12', 'b': 'b2', 'p': {'x': 'y'}},
            {'a': 'a13', 'b': 'b2', 'p': {'x': 'y'}},
        ]
        b = [
            {'a': 'a21', 'b': 'b1', 'p': {'x': 'x1'}},
            {'a': 'a22', 'b': 'b3', 'p': {'x': 'y'}},
            {'a': 'a23', 'b': 'b2', 'p': {'x': 'y'}},
        ]
        filters = {
            libracmp.All(): {'a': IgnoreComparator},
            0: {'a': IgnoreComparator, 'p': {'x': IgnoreComparator}},
            1: {'a': IgnoreComparator, 'b': IgnoreComparator}
        }
        comp = Comparator(a, b, filters=filters)
        self.assertTrue(comp.result)
