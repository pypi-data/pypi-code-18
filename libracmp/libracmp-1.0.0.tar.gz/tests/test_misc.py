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
from libracmp import All as NewAll
import libracmp
import copy


class TestMisc(TestCase):

    def test_singleton_all_is(self):
        x = libracmp.All()
        y = libracmp.All()
        self.assertIs(x, y)

    def test_singleton_all_id(self):
        x = id(libracmp.All())
        y = id(libracmp.All())
        self.assertEqual(x, y)

    def test_singleton_all_str(self):
        x = libracmp.All()
        exp = '<%all>'
        self.assertEqual(str(x), exp)

    def test_singleton_all_repr(self):
        x = libracmp.All()
        exp = '<%all>'
        self.assertEqual(repr(x), exp)

    def test_singleton_all_key(self):
        d = {libracmp.All(): 'x'}
        exp = 'x'
        self.assertEqual(d.get(libracmp.All()), exp)

    def test_singleton_all_in(self):
        d = {libracmp.All(): 'x'}
        self.assertIn(libracmp.All(), d)

    def test_singleton_all_imports_id(self):
        x = id(libracmp.All())
        y = id(NewAll())
        self.assertEqual(x, y)

    def test_singleton_all_copy_id(self):
        x = libracmp.All()
        y = copy.copy(x)
        self.assertEqual(id(x), id(y))

    def test_singleton_all_deepcopy_id(self):
        x = libracmp.All()
        y = copy.deepcopy(x)
        self.assertEqual(id(x), id(y))

