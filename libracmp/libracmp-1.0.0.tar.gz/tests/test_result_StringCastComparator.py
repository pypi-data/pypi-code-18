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
from libracmp.StringCastComparator import StringCastComparator


class TestResultStringCastComparator(TestCase):
    # test result
    # ---------------------------------------------------------
    # None
    def test_result_none_eq(self):
        a, b = None, None
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_none_int0_neq(self):
        a, b = None, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_int1_neq(self):
        a, b = None, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_intn1_neq(self):
        a, b = None, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_float0_neq(self):
        a, b = None, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_float1_neq(self):
        a, b = None, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_floatn1_neq(self):
        a, b = None, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_strNone_eq(self):
        a, b = None, 'None'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_none_str_empty_neq(self):
        a, b = None, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_uniNone_eq(self):
        a, b = None, u'None'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_none_uni_empty_neq(self):
        a, b = None, u''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_true_neq(self):
        a, b = None, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_none_false_neq(self):
        a, b = None, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    # ---------------------------------------------------------
    # True
    def test_result_true_eq(self):
        a, b = True, True
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_true_false_neq(self):
        a, b = True, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_int0_neq(self):
        a, b = True, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_int1_neq(self):
        a, b = True, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_intn1_neq(self):
        a, b = True, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_float0_neq(self):
        a, b = True, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_float1_neq(self):
        a, b = True, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_floatn1_neq(self):
        a, b = True, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_strEmpty_neq(self):
        a, b = True, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_strTrue_eq(self):
        a, b = True, 'True'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_true_strTest_neq(self):
        a, b = True, 'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_uniEmpty_neq(self):
        a, b = True, u''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_true_uniTrue_eq(self):
        a, b = True, u'True'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_true_uniTest_neq(self):
        a, b = True, u'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    # ---------------------------------------------------------
    # False
    def test_result_false_eq(self):
        a, b = False, False
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_false_true_neq(self):
        a, b = False, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_int0_neq(self):
        a, b = False, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_int1_neq(self):
        a, b = False, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_intn1_neq(self):
        a, b = False, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_float0_neq(self):
        a, b = False, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_float1_neq(self):
        a, b = False, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_floatn1_neq(self):
        a, b = False, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_strEmpty_neq(self):
        a, b = False, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_strFalse_eq(self):
        a, b = False, 'False'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_false_strTest_neq(self):
        a, b = False, 'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_uniEmpty_neq(self):
        a, b = False, u''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_false_uniFalse_eq(self):
        a, b = False, u'False'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_false_uniTest_neq(self):
        a, b = False, u'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    # ---------------------------------------------------------
    # int
    def test_result_int1_int0_neq(self):
        a, b = 1, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_int1_eq(self):
        a, b = 1, 1
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_intn1_intn1_eq(self):
        a, b = -1, -1
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_int1_intn1_neq(self):
        a, b = 1, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int0_float0_neq(self):
        a, b = 0, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_float0_neq(self):
        a, b = 1, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_float1_neq(self):
        a, b = 1, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_intn1_floatn1_neq(self):
        a, b = -1, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_floatn1_neq(self):
        a, b = 1, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int0_none_neq(self):
        a, b = 0, None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_none_neq(self):
        a, b = 1, None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int0_true_neq(self):
        a, b = 0, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int0_false_neq(self):
        a, b = 0, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_true_neq(self):
        a, b = 1, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_false_neq(self):
        a, b = 1, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_int1_str1_eq(self):
        a, b = 1, '1'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_int1_uni1_eq(self):
        a, b = 1, u'1'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    # ---------------------------------------------------------
    # float
    def test_result_float0_float0_eq(self):
        a, b = 0.0, 0.0
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_float1_float1_eq(self):
        a, b = 1.0, 1.0
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_floatn1_floatn1_eq(self):
        a, b = -1.0, -1.0
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_float0_floatn1_neq(self):
        a, b = 0.0, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_float1_neq(self):
        a, b = 0.0, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_float0_neq(self):
        a, b = 1.0, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_floatn1_neq(self):
        a, b = 1.0, -1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_float0_neq(self):
        a, b = -1.0, 0.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_float1_neq(self):
        a, b = -1.0, 1.0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_int0_neq(self):
        a, b = 0.0, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_int1_neq(self):
        a, b = 1.0, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_intn1_neq(self):
        a, b = -1.0, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_intn1_neq(self):
        a, b = 0.0, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_int1_neq(self):
        a, b = 0.0, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_int0_neq(self):
        a, b = 1.0, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_intn1_neq(self):
        a, b = 1.0, -1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_int0_neq(self):
        a, b = -1.0, 0
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_int1_neq(self):
        a, b = -1.0, 1
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_strEmpty_neq(self):
        a, b = 0.0, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_str0_eq(self):
        a, b = 0.0, '0.0'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_float0_strTest_neq(self):
        a, b = 0.0, 'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_strEmpty_neq(self):
        a, b = 1.0, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_str1_eq(self):
        a, b = 1.0, '1.0'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_float1_strTest_neq(self):
        a, b = 1.0, 'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_strEmpty_neq(self):
        a, b = -1.0, ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_strn1_eq(self):
        a, b = -1.0, '-1.0'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_floatn1_strTest_neq(self):
        a, b = -1.0, 'Test'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_none_neq(self):
        a, b = 0.0, None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_none_neq(self):
        a, b = 1.0, None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_none_neq(self):
        a, b = -1.0, None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_true_neq(self):
        a, b = 0.0, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_true_neq(self):
        a, b = 1.0, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_true_neq(self):
        a, b = -1.0, True
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float0_false_neq(self):
        a, b = 0.0, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_float1_false_neq(self):
        a, b = 1.0, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_floatn1_false_neq(self):
        a, b = -1.0, False
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    # ---------------------------------------------------------
    # str
    def test_result_strEmpty_strEmpty_eq(self):
        a, b = '', ''
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_stra_strEmpty_neq(self):
        a, b = 'a', ''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_stra_stra_eq(self):
        a, b = 'a', 'a'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_stra_strb_neq(self):
        a, b = 'a', 'b'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_strEmpty_uniEmpty_eq(self):
        a, b = '', u''
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_stra_uniEmpty_neq(self):
        a, b = 'a', u''
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_stra_unia_eq(self):
        a, b = 'a', u'a'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_stra_unib_neq(self):
        a, b = 'a', u'b'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_str_empty_none_neq(self):
        a, b = '', None
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_str_none_eq(self):
        a, b = 'None', None
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_str_int_eq(self):
        a, b = '1', 1
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_str_float_eq(self):
        a, b = '1.0', 1.0
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    # ---------------------------------------------------------
    # unicode
    def test_result_uniEmpty_uniEmpty_eq(self):
        a, b = u'', u''
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_uniEmpty_unia_neq(self):
        a, b = u'', u'a'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_unia_unia_eq(self):
        a, b = u'a', u'a'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_unia_unib_neq(self):
        a, b = u'a', u'b'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_uniEmpty_strEmpty_eq(self):
        a, b = u'', ''
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_uniEmpty_stra_neq(self):
        a, b = u'', 'a'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)

    def test_result_unia_stra_eq(self):
        a, b = u'a', 'a'
        comp = StringCastComparator(a, b)
        self.assertTrue(comp.result)

    def test_result_unia_strb_neq(self):
        a, b = u'a', 'b'
        comp = StringCastComparator(a, b)
        self.assertFalse(comp.result)
