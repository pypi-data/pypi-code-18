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

from libracmp.AbstractComparator import AbstractComparator
from libracmp.IgnoreComparator import IgnoreComparator
from libracmp.RelaxedComparator import RelaxedComparator


class TestCompatibleTypes(TestCase):
    # abstract comparator
    def test_abstract_comparator_pos(self):
        a = 'a'
        b = 'b'
        comp = AbstractComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_abstract_comparator_true_false_neg(self):
        a = True
        b = False
        comp = AbstractComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_abstract_comparator_string_uni_pos(self):
        a = 'a'
        b = u'b'
        comp = AbstractComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    def test_abstract_comparator_str_int_neg(self):
        a = 'a'
        b = 1
        comp = AbstractComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    def test_abstract_comparator_none_int_neg(self):
        a = None
        b = 1
        comp = AbstractComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    def test_abstract_comparator_float_int_neg(self):
        a = 1.0
        b = 1
        comp = AbstractComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    # relaxed comparator
    def test_relaxed_comparator_pos(self):
        a = 'a'
        b = 'b'
        comp = RelaxedComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_relaxed_comparator_true_false_neg(self):
        a = True
        b = False
        comp = RelaxedComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_relaxed_comparator_string_uni_pos(self):
        a = 'a'
        b = u'b'
        comp = RelaxedComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    def test_relaxed_comparator_str_int_neg(self):
        a = 'a'
        b = 1
        comp = RelaxedComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    def test_relaxed_comparator_none_int_pos(self):
        a = None
        b = 1
        comp = RelaxedComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_relaxed_comparator_float_int_neg(self):
        a = 1.0
        b = 1
        comp = RelaxedComparator(a, b)
        self.assertFalse(comp._compatible_types(a, b))

    # ignore comparator
    def test_ignore_comparator_pos(self):
        a = 'a'
        b = 'b'
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_ignore_comparator_true_false_pos(self):
        a = True
        b = False
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_ignore_comparator_string_uni_pos(self):
        a = 'a'
        b = u'b'
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_ignore_comparator_str_int_pos(self):
        a = 'a'
        b = 1
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_ignore_comparator_none_int_pos(self):
        a = None
        b = 1
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))

    def test_ignore_comparator_float_int_pos(self):
        a = 1.0
        b = 1
        comp = IgnoreComparator(a, b)
        self.assertTrue(comp._compatible_types(a, b))
