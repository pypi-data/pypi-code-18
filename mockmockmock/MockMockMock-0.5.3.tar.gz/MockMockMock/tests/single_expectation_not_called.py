# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class SingleExpectationNotCalledTestCase(unittest.TestCase):
    def setUp(self):
        super(SingleExpectationNotCalledTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.mock = self.mocks.create("mock")

    def test_method_call_with_bad_argument(self):
        self.mock.expect.foobar(42)
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mock.object.foobar(43)
        self.assertEqual(str(cm.exception), "mock.foobar called with bad arguments (43,) {}")

    def test_method_call_with_bad_name(self):
        self.mock.expect.foobar()
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mock.object.barbaz()
        self.assertEqual(str(cm.exception), "mock.barbaz called instead of mock.foobar")

    def test_property_with_bad_name(self):
        self.mock.expect.foobar.and_return(42)
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mock.object.barbaz
        self.assertEqual(str(cm.exception), "mock.barbaz called instead of mock.foobar")

    def test_method_not_called(self):
        self.mock.expect.foobar()
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.foobar not called")
        self.mock.object.foobar()
        self.mocks.tearDown()

    def test_property_not_called(self):
        self.mock.expect.foobar
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.foobar not called")
        self.mock.object.foobar
        self.mocks.tearDown()

    def test_property_not_called_in_ordered_group(self):
        self.mock.expect.foobar
        self.mock.expect.barbaz
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.foobar or mock.barbaz not called")  # @todo Remove "or mock.barbaz"
        self.mock.object.foobar
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.barbaz not called")
        self.mock.object.barbaz
        self.mocks.tearDown()

    def test_property_not_called_in_unordered_group(self):
        with self.mocks.unordered:
            self.mock.expect.foobar
            self.mock.expect.barbaz
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.foobar or mock.barbaz not called")
        self.mock.object.foobar
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "mock.barbaz not called")
        self.mock.object.barbaz
        self.mocks.tearDown()
