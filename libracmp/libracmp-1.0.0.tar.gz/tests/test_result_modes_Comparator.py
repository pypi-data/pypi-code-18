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
import libracmp.exceptions
from libracmp.Comparator import Comparator


class TestResultComparator(TestCase):

    # lists
    def test_result_lista_listNone_default_neq(self):
        a = ['a']
        b = [None]
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_lista_listNone_strict_neq(self):
        a = ['a']
        b = [None]
        comp = Comparator(a, b, mode=libracmp.MODE_STRICT)
        self.assertFalse(comp.result)

    def test_result_lista_listNone_relaxed_eq(self):
        a = ['a']
        b = [None]
        comp = Comparator(a, b, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)

    def test_result_list1_listf1_typestrict_neq(self):
        a = [1]
        b = [1.0]
        comp = Comparator(a, b, mode=libracmp.MODE_TYPESTRICT)
        self.assertFalse(comp.result)

    def test_result_lista_listfb_ignore_eq(self):
        a = ['a']
        b = ['b']
        comp = Comparator(a, b, mode=libracmp.MODE_IGNORE)
        self.assertTrue(comp.result)

    def test_result_mode_default_none_lists_exc(self):
        a = ['a']
        b = ['b']
        mode_default_none = {
            'default': None,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = Comparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result

    def test_result_mode_default_type_error_lists_exc(self):
        a = ['a']
        b = ['b']
        mode_default_none = {
            'default': object,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = Comparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result

    # dicts
    def test_result_dicta_dictNone_default_neq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_dicta_dictNone_strict_neq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = Comparator(a, b, mode=libracmp.MODE_STRICT)
        self.assertFalse(comp.result)

    def test_result_dicta_dictNone_relaxed_eq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = Comparator(a, b, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)

    def test_result_dict1_dictf1_typestrict_neq(self):
        a = {'a': 1}
        b = {'a': 1.0}
        comp = Comparator(a, b, mode=libracmp.MODE_TYPESTRICT)
        self.assertFalse(comp.result)

    def test_result_dicta_dictfb_ignore_eq(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        comp = Comparator(a, b, mode=libracmp.MODE_IGNORE)
        self.assertTrue(comp.result)

    def test_result_mode_default_none_dicts_exc(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        mode_default_none = {
            'default': None,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = Comparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result

    def test_result_mode_default_type_error_dicts_exc(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        mode_default_none = {
            'default': object,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = Comparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result

    # mixed
    def test_result_listdict_listdict_none_default_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': None}}]
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_none_strict_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': None}}]
        comp = Comparator(a, b, mode=libracmp.MODE_STRICT)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_none_relaxed_eq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': None}}]
        comp = Comparator(a, b, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)

    def test_result_listdict_listdict_typestrict_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': 2.0}}]
        comp = Comparator(a, b, mode=libracmp.MODE_TYPESTRICT)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_ignore_eq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': 'x'}}]
        comp = Comparator(a, b, mode=libracmp.MODE_IGNORE)
        self.assertTrue(comp.result)
