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


class TestDiffComparator(TestCase):

    @staticmethod
    def do_merge_dicts(a, b):
        return {k: (a.get(k), b.get(k)) for k in set(a.keys()+b.keys())}

    # test_diff
    # ---------------------------------------------------------
    def test_diff_none_eq(self):
        a, b = {'k': None}, {'k': None}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_int0_neq(self):
        a, b = {'k': None}, {'k': 0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_int1_neq(self):
        a, b = {'k': None}, {'k': 1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_intn1_neq(self):
        a, b = {'k': None}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_float0_neq(self):
        a, b = {'k': None}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_float1_neq(self):
        a, b = {'k': None}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_floatn1_neq(self):
        a, b = {'k': None}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_strNone_neq(self):
        a, b = {'k': None}, {'k': 'None'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_str_empty_neq(self):
        a, b = {'k': None}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_uniNone_neq(self):
        a, b = {'k': None}, {'k': u'None'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_uni_empty_neq(self):
        a, b = {'k': None}, {'k': u''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_true_neq(self):
        a, b = {'k': None}, {'k': True}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_none_false_neq(self):
        a, b = {'k': None}, {'k': False}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # True
    def test_diff_true_eq(self):
        a, b = {'k': True}, {'k': True}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_false_neq(self):
        a, b = {'k': True}, {'k': False}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_int0_neq(self):
        a, b = {'k': True}, {'k': 0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_int1_eq(self):
        a, b = {'k': True}, {'k': 1}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_intn1_neq(self):
        a, b = {'k': True}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_float0_neq(self):
        a, b = {'k': True}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_float1_eq(self):
        a, b = {'k': True}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_floatn1_neq(self):
        a, b = {'k': True}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_strEmpty_neq(self):
        a, b = {'k': True}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_strTrue_neq(self):
        a, b = {'k': True}, {'k': 'True'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_strTest_neq(self):
        a, b = {'k': True}, {'k': 'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_uniEmpty_neq(self):
        a, b = {'k': True}, {'k': u''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_uniTrue_neq(self):
        a, b = {'k': True}, {'k': u'True'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_true_uniTest_neq(self):
        a, b = {'k': True}, {'k': u'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # False
    def test_diff_false_eq(self):
        a, b = {'k': False}, {'k': False}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_true_neq(self):
        a, b = {'k': False}, {'k': True}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_int0_eq(self):
        a, b = {'k': False}, {'k': 0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_int1_neq(self):
        a, b = {'k': False}, {'k': 1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_intn1_neq(self):
        a, b = {'k': False}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_float0_eq(self):
        a, b = {'k': False}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_float1_neq(self):
        a, b = {'k': False}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_floatn1_neq(self):
        a, b = {'k': False}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_strEmpty_neq(self):
        a, b = {'k': False}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_strFalse_neq(self):
        a, b = {'k': False}, {'k': 'False'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_strTest_neq(self):
        a, b = {'k': False}, {'k': 'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_uniEmpty_neq(self):
        a, b = {'k': False}, {'k': u''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_uniFalse_neq(self):
        a, b = {'k': False}, {'k': u'False'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_false_uniTest_neq(self):
        a, b = {'k': False}, {'k': u'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # int
    def test_diff_int1_int0_neq(self):
        a, b = {'k': 1}, {'k': 0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int1_int1_eq(self):
        a, b = {'k': 1}, {'k': 1}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_intn1_intn1_eq(self):
        a, b = {'k': -1}, {'k': -1}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_intn1_neq(self):
        a, b = {'k': 1}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int0_float0_eq(self):
        a, b = {'k': 0}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_float0_neq(self):
        a, b = {'k': 1}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int1_float1_eq(self):
        a, b = {'k': 1}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_intn1_floatn1_eq(self):
        a, b = {'k': -1}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_floatn1_neq(self):
        a, b = {'k': 1}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int0_none_neq(self):
        a, b = {'k': 0}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int1_none_neq(self):
        a, b = {'k': 1}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int0_true_neq(self):
        a, b = {'k': 0}, {'k': True}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int0_false_eq(self):
        a, b = {'k': 0}, {'k': False}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_true_eq(self):
        a, b = {'k': 1}, {'k': True}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_false_neq(self):
        a, b = {'k': 1}, {'k': False}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int1_str1_neq(self):
        a, b = {'k': 1}, {'k': '1'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_int1_uni1_neq(self):
        a, b = {'k': 1}, {'k': u'1'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # float
    def test_diff_float0_float0_eq(self):
        a, b = {'k': 0.0}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_float1_eq(self):
        a, b = {'k': 1.0}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_floatn1_eq(self):
        a, b = {'k': -1.0}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float0_floatn1_neq(self):
        a, b = {'k': 0.0}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_float1_neq(self):
        a, b = {'k': 0.0}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_float0_neq(self):
        a, b = {'k': 1.0}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_floatn1_neq(self):
        a, b = {'k': 1.0}, {'k': -1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_float0_neq(self):
        a, b = {'k': -1.0}, {'k': 0.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_float1_neq(self):
        a, b = {'k': -1.0}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_int0_eq(self):
        a, b = {'k': 0.0}, {'k': 0}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_int1_eq(self):
        a, b = {'k': 1.0}, {'k': 1}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_intn1_eq(self):
        a, b = {'k': -1.0}, {'k': -1}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float0_intn1_neq(self):
        a, b = {'k': 0.0}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_int1_neq(self):
        a, b = {'k': 0.0}, {'k': 1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_int0_neq(self):
        a, b = {'k': 1.0}, {'k': 0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_intn1_neq(self):
        a, b = {'k': 1.0}, {'k': -1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_int0_neq(self):
        a, b = {'k': -1.0}, {'k': 0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_int1_neq(self):
        a, b = {'k': -1.0}, {'k': 1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_strEmpty_neq(self):
        a, b = {'k': 0.0}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_str0_neq(self):
        a, b = {'k': 0.0}, {'k': '0.0'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_strTest_neq(self):
        a, b = {'k': 0.0}, {'k': 'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_strEmpty_neq(self):
        a, b = {'k': 1.0}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_str1_neq(self):
        a, b = {'k': 1.0}, {'k': '1.0'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_strTest_neq(self):
        a, b = {'k': 1.0}, {'k': 'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_strEmpty_neq(self):
        a, b = {'k': -1.0}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_strn1_neq(self):
        a, b = {'k': -1.0}, {'k': '-1.0'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_strTest_neq(self):
        a, b = {'k': -1.0}, {'k': 'Test'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_none_neq(self):
        a, b = {'k': 0.0}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_none_neq(self):
        a, b = {'k': 1.0}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_none_neq(self):
        a, b = {'k': -1.0}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_true_neq(self):
        a, b = {'k': 0.0}, {'k': True}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float1_true_eq(self):
        a, b = {'k': 1.0}, {'k': True}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_true_neq(self):
        a, b = {'k': -1.0}, {'k': True}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_float0_false_eq(self):
        a, b = {'k': 0.0}, {'k': False}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_false_neq(self):
        a, b = {'k': 1.0}, {'k': False}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_floatn1_false_neq(self):
        a, b = {'k': -1.0}, {'k': False}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # str
    def test_diff_strEmpty_strEmpty_eq(self):
        a, b = {'k': ''}, {'k': ''}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_strEmpty_neq(self):
        a, b = {'k': 'a'}, {'k': ''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_stra_stra_eq(self):
        a, b = {'k': 'a'}, {'k': 'a'}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_strb_neq(self):
        a, b = {'k': 'a'}, {'k': 'b'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_strEmpty_uniEmpty_eq(self):
        a, b = {'k': ''}, {'k': u''}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_uniEmpty_neq(self):
        a, b = {'k': 'a'}, {'k': u''}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_stra_unia_eq(self):
        a, b = {'k': 'a'}, {'k': u'a'}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_unib_neq(self):
        a, b = {'k': 'a'}, {'k': u'b'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_str_empty_none_neq(self):
        a, b = {'k': ''}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_str_none_neq(self):
        a, b = {'k': 'None'}, {'k': None}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_str_int_neq(self):
        a, b = {'k': '1'}, {'k': 1}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_str_float_neq(self):
        a, b = {'k': '1.0'}, {'k': 1.0}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    # ---------------------------------------------------------
    # unicode
    def test_diff_uniEmpty_uniEmpty_eq(self):
        a, b = {'k': u''}, {'k': u''}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_uniEmpty_unia_neq(self):
        a, b = {'k': u''}, {'k': u'a'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_unia_unia_eq(self):
        a, b = {'k': u'a'}, {'k': u'a'}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_unia_unib_neq(self):
        a, b = {'k': u'a'}, {'k': u'b'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_uniEmpty_strEmpty_eq(self):
        a, b = {'k': u''}, {'k': ''}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_uniEmpty_stra_neq(self):
        a, b = {'k': u''}, {'k': 'a'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))

    def test_diff_unia_stra_eq(self):
        a, b = {'k': u'a'}, {'k': 'a'}
        comp = Comparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_unia_strb_neq(self):
        a, b = {'k': u'a'}, {'k': 'b'}
        comp = Comparator(a, b)
        self.assertEquals(comp.diff, self.do_merge_dicts(a, b))
