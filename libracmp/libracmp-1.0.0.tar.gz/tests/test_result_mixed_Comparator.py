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


class TestResultMixedComparator(TestCase):

    def test_result_stra_stra_eq(self):
        a = 'a'
        b = 'a'
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listEmpty_listEmpty_eq(self):
        a = []
        b = []
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listStra_listStra_eq(self):
        a = ['a']
        b = ['a']
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_dictEmpty_dictEmpty_eq(self):
        a = {}
        b = {}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_dictStra_dictStra_eq(self):
        a = {'a': 'a'}
        b = {'a': 'a'}
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listStra_dictStra_neq(self):
        a = ['a']
        b = {'a': 'a'}
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_stra_neq(self):
        a = ['a']
        b = 'a'
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listStra_None_neq(self):
        a = ['a']
        b = None
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_dictStra_stra_neq(self):
        a = {'a': 'a'}
        b = 'a'
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_dictStra_None_neq(self):
        a = {'a': 'a'}
        b = None
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_eq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': 2}}]
        comp = Comparator(a, b)
        self.assertTrue(comp.result)

    def test_result_listdict_listdict_3_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': 3}}]
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_missing_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1}}]
        comp = Comparator(a, b)
        self.assertFalse(comp.result)

    def test_result_listdict_listdict_none_neq(self):
        a = [{'x': {'a': 1, 'b': 2}}]
        b = [{'x': {'a': 1, 'b': None}}]
        comp = Comparator(a, b)
        self.assertFalse(comp.result)


