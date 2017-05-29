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
from libracmp.DictComparator import DictComparator


class TestResultDictComparator(TestCase):

    def test_result_dicta_dictNone_default_neq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = DictComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_dicta_dictNone_strict_neq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = DictComparator(a, b, mode=libracmp.MODE_STRICT)
        self.assertFalse(comp.result)

    def test_result_dicta_dictNone_relaxed_eq(self):
        a = {'a': 'a'}
        b = {'a': None}
        comp = DictComparator(a, b, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)

    def test_result_dict1_dictf1_typestrict_neq(self):
        a = {'a': 1}
        b = {'a': 1.0}
        comp = DictComparator(a, b, mode=libracmp.MODE_TYPESTRICT)
        self.assertFalse(comp.result)

    def test_result_dicta_dictfb_ignore_eq(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        comp = DictComparator(a, b, mode=libracmp.MODE_IGNORE)
        self.assertTrue(comp.result)

    def test_result_mode_default_none_exc(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        mode_default_none = {
            'default': None,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = DictComparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result

    def test_result_mode_default_type_error_exc(self):
        a = {'a': 'a'}
        b = {'a': 'b'}
        mode_default_none = {
            'default': object,
            'list': libracmp.ListComparator.ListComparator,
            'dict': libracmp.DictComparator.DictComparator,
        }
        comp = DictComparator(a, b, mode=mode_default_none)
        with self.assertRaises(libracmp.exceptions.CannotCompareError):
            _ = comp.result
