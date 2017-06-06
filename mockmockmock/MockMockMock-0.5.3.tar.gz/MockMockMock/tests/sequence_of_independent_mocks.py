# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class SequenceOfIndependentMocksTestCase(unittest.TestCase):
    def setUp(self):
        super(SequenceOfIndependentMocksTestCase, self).setUp()
        self.mocks1 = MockMockMock.Engine()
        self.mocks2 = MockMockMock.Engine()
        self.m1 = self.mocks1.create("m1")
        self.m2 = self.mocks2.create("m2")

    def test_same_order_sequence(self):
        self.m1.expect.foobar(42)
        self.m2.expect.foobar(43)
        self.m1.object.foobar(42)
        self.m2.object.foobar(43)
        self.mocks1.tearDown()
        self.mocks2.tearDown()

    def test_other_order_sequence(self):
        self.m1.expect.foobar(42)
        self.m2.expect.foobar(43)
        self.m2.object.foobar(43)
        self.m1.object.foobar(42)
        self.mocks1.tearDown()
        self.mocks2.tearDown()
