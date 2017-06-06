# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class OrderingTestCase(unittest.TestCase):
    def setUp(self):
        super(OrderingTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.mock = self.mocks.create("mock")

    def test_unordered_group_of_same_method(self):
        with self.mocks.unordered:
            self.mock.expect.foobar(1).and_return(11)
            self.mock.expect.foobar(1).and_return(13)
            self.mock.expect.foobar(2).and_return(12)
            self.mock.expect.foobar(1).and_return(14)
        self.assertEqual(self.mock.object.foobar(2), 12)
        self.assertEqual(self.mock.object.foobar(1), 11)
        self.assertEqual(self.mock.object.foobar(1), 13)
        self.assertEqual(self.mock.object.foobar(1), 14)
        self.mocks.tearDown()

    # @todo Allow unordered property and method calls on the same name: difficult
    def test_unordered_group_of_same_method_and_property(self):
        with self.assertRaises(MockMockMock.MockException) as cm:
            with self.mocks.unordered:
                self.mock.expect.foobar()
                self.mock.expect.foobar
            self.mock.object.foobar  # @todo Fail fast: raise exception during the expect phase. Same in next test
        self.assertEqual(str(cm.exception), "mock.foobar is expected as a property and as a method call in an unordered group")

    def test_unordered_group_of_same_property_and_method(self):
        with self.assertRaises(MockMockMock.MockException) as cm:
            with self.mocks.unordered:
                self.mock.expect.foobar
                self.mock.expect.foobar()
            self.mock.object.foobar()
        self.assertEqual(str(cm.exception), "mock.foobar is expected as a property and as a method call in an unordered group")
