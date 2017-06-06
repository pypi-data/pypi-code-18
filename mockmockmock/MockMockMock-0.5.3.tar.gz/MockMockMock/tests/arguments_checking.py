# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock
import MockMockMock.arguments_checking


class ArgumentsCheckersTestCase(unittest.TestCase):
    def test_checker_is_used_by_call(self):
        # We use a myMock...
        checker = MockMockMock.Engine().create("checker")
        checker.expect((12,), {}).and_return(True)
        checker.expect((13,), {}).and_return(False)

        # ...to test a mock!
        m = MockMockMock.Engine().create("m")
        m.expect.foobar.with_arguments(checker.object).and_return(42)
        m.expect.foobar.with_arguments(checker.object).and_return(43)
        self.assertEqual(m.object.foobar(12), 42)
        with self.assertRaises(MockMockMock.MockException) as cm:
            m.object.foobar(13)
        self.assertEqual(str(cm.exception), "m.foobar called with bad arguments (13,) {}")

    # @todo def test_identity_checker(self):
    # @todo def test_type_checker(self):
    # @todo def test_range_checker(self):

    def test_equality_checker(self):
        c = MockMockMock.arguments_checking.Equality((1, 2, 3), {1: 1, 2: 2, 3: 3})
        self.assertTrue(c((1, 2, 3), {1: 1, 2: 2, 3: 3}))
        self.assertFalse(c((1, 2, 3), {1: 1, 2: 2, 3: 4}))
        self.assertFalse(c((1, 2, 4), {1: 1, 2: 2, 3: 3}))
