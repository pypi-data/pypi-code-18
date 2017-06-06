# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class SequenceOfLinkedMocksTestCase(unittest.TestCase):
    def setUp(self):
        super(SequenceOfLinkedMocksTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.m1 = self.mocks.create("m1")
        self.m2 = self.mocks.create("m2")

    def test_short_correct_sequence(self):
        self.m1.expect.foobar(42)
        self.m2.expect.foobar(43)
        self.m1.object.foobar(42)
        self.m2.object.foobar(43)
        self.mocks.tearDown()

    def test_short_inverted_sequence(self):
        self.m1.expect.foobar(42)
        self.m2.expect.foobar(43)
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.m2.object.foobar(43)
        self.assertEqual(str(cm.exception), "m2.foobar called instead of m1.foobar")
