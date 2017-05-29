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
from libracmp.RelaxedComparator import RelaxedComparator


class TestDiffRelaxedComparator(TestCase):
    # test_diff
    # ---------------------------------------------------------
    def test_diff_none_eq(self):
        a, b = None, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_int0_eq(self):
        a, b = None, 0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_int1_eq(self):
        a, b = None, 1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_intn1_eq(self):
        a, b = None, -1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_float0_eq(self):
        a, b = None, 0.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_float1_eq(self):
        a, b = None, 1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_floatn1_eq(self):
        a, b = None, -1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_strNone_eq(self):
        a, b = None, 'None'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_str_empty_eq(self):
        a, b = None, ''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_uniNone_eq(self):
        a, b = None, u'None'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_uni_empty_eq(self):
        a, b = None, u''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_true_eq(self):
        a, b = None, True
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_none_false_eq(self):
        a, b = None, False
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    # ---------------------------------------------------------
    # True
    def test_diff_true_eq(self):
        a, b = True, True
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_false_neq(self):
        a, b = True, False
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_int0_neq(self):
        a, b = True, 0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_int1_eq(self):
        a, b = True, 1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_intn1_neq(self):
        a, b = True, -1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_float0_neq(self):
        a, b = True, 0.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_float1_eq(self):
        a, b = True, 1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_true_floatn1_neq(self):
        a, b = True, -1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_strEmpty_neq(self):
        a, b = True, ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_strTrue_neq(self):
        a, b = True, 'True'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_strTest_neq(self):
        a, b = True, 'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_uniEmpty_neq(self):
        a, b = True, u''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_uniTrue_neq(self):
        a, b = True, u'True'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_true_uniTest_neq(self):
        a, b = True, u'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    # ---------------------------------------------------------
    # False
    def test_diff_false_eq(self):
        a, b = False, False
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_true_neq(self):
        a, b = False, True
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_int0_eq(self):
        a, b = False, 0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_int1_neq(self):
        a, b = False, 1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_intn1_neq(self):
        a, b = False, -1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_float0_eq(self):
        a, b = False, 0.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_false_float1_neq(self):
        a, b = False, 1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_floatn1_neq(self):
        a, b = False, -1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_strEmpty_neq(self):
        a, b = False, ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_strFalse_neq(self):
        a, b = False, 'False'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_strTest_neq(self):
        a, b = False, 'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_uniEmpty_neq(self):
        a, b = False, u''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_uniFalse_neq(self):
        a, b = False, u'False'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_false_uniTest_neq(self):
        a, b = False, u'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    # ---------------------------------------------------------
    # int
    def test_diff_int1_int0_neq(self):
        a, b = 1, 0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int1_int1_eq(self):
        a, b = 1, 1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_intn1_intn1_eq(self):
        a, b = -1, -1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_intn1_neq(self):
        a, b = 1, -1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int0_float0_eq(self):
        a, b = 0, 0.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_float0_neq(self):
        a, b = 1, 0.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int1_float1_eq(self):
        a, b = 1, 1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_intn1_floatn1_eq(self):
        a, b = -1, -1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_floatn1_neq(self):
        a, b = 1, -1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int0_none_eq(self):
        a, b = 0, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_none_eq(self):
        a, b = 1, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int0_true_neq(self):
        a, b = 0, True
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int0_false_eq(self):
        a, b = 0, False
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_true_eq(self):
        a, b = 1, True
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_int1_false_neq(self):
        a, b = 1, False
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int1_str1_neq(self):
        a, b = 1, '1'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_int1_uni1_neq(self):
        a, b = 1, u'1'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    # ---------------------------------------------------------
    # float
    def test_diff_float0_float0_eq(self):
        a, b = 0.0, 0.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_float1_eq(self):
        a, b = 1.0, 1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_floatn1_eq(self):
        a, b = -1.0, -1.0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float0_floatn1_neq(self):
        a, b = 0.0, -1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_float1_neq(self):
        a, b = 0.0, 1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_float0_neq(self):
        a, b = 1.0, 0.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_floatn1_neq(self):
        a, b = 1.0, -1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_float0_neq(self):
        a, b = -1.0, 0.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_float1_neq(self):
        a, b = -1.0, 1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_int0_eq(self):
        a, b = 0.0, 0
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_int1_eq(self):
        a, b = 1.0, 1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_intn1_eq(self):
        a, b = -1.0, -1
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float0_intn1_neq(self):
        a, b = 0.0, -1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_int1_neq(self):
        a, b = 0.0, 1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_int0_neq(self):
        a, b = 1.0, 0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_intn1_neq(self):
        a, b = 1.0, -1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_int0_neq(self):
        a, b = -1.0, 0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_int1_neq(self):
        a, b = -1.0, 1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_strEmpty_neq(self):
        a, b = 0.0, ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_str0_neq(self):
        a, b = 0.0, '0.0'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_strTest_neq(self):
        a, b = 0.0, 'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_strEmpty_neq(self):
        a, b = 1.0, ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_str1_neq(self):
        a, b = 1.0, '1.0'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_strTest_neq(self):
        a, b = 1.0, 'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_strEmpty_neq(self):
        a, b = -1.0, ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_strn1_neq(self):
        a, b = -1.0, '-1.0'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_strTest_neq(self):
        a, b = -1.0, 'Test'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_none_eq(self):
        a, b = 0.0, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_none_eq(self):
        a, b = 1.0, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_none_eq(self):
        a, b = -1.0, None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float0_true_neq(self):
        a, b = 0.0, True
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float1_true_eq(self):
        a, b = 1.0, True
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_floatn1_true_neq(self):
        a, b = -1.0, True
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_float0_false_eq(self):
        a, b = 0.0, False
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_float1_false_neq(self):
        a, b = 1.0, False
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_floatn1_false_neq(self):
        a, b = -1.0, False
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    # ---------------------------------------------------------
    # str
    def test_diff_strEmpty_strEmpty_eq(self):
        a, b = '', ''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_strEmpty_neq(self):
        a, b = 'a', ''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_stra_stra_eq(self):
        a, b = 'a', 'a'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_strb_neq(self):
        a, b = 'a', 'b'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_strEmpty_uniEmpty_eq(self):
        a, b = '', u''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_uniEmpty_neq(self):
        a, b = 'a', u''
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_stra_unia_eq(self):
        a, b = 'a', u'a'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_stra_unib_neq(self):
        a, b = 'a', u'b'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_str_empty_none_eq(self):
        a, b = '', None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_str_none_eq(self):
        a, b = 'None', None
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_str_int_neq(self):
        a, b = '1', 1
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_str_float_neq(self):
        a, b = '1.0', 1.0
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    # ---------------------------------------------------------
    # unicode
    def test_diff_uniEmpty_uniEmpty_eq(self):
        a, b = u'', u''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_uniEmpty_unia_neq(self):
        a, b = u'', u'a'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_unia_unia_eq(self):
        a, b = u'a', u'a'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_unia_unib_neq(self):
        a, b = u'a', u'b'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_uniEmpty_strEmpty_eq(self):
        a, b = u'', ''
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_uniEmpty_stra_neq(self):
        a, b = u'', 'a'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))

    def test_diff_unia_stra_eq(self):
        a, b = u'a', 'a'
        comp = RelaxedComparator(a, b)
        self.assertIsNone(comp.diff)

    def test_diff_unia_strb_neq(self):
        a, b = u'a', 'b'
        comp = RelaxedComparator(a, b)
        self.assertEquals(comp.diff, (a, b))
