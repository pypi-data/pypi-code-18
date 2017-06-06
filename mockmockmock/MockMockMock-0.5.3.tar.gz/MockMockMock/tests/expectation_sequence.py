# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class ExpectationSequenceTestCase(unittest.TestCase):
    def setUp(self):
        super(ExpectationSequenceTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.mock = self.mocks.create("mock")

    def test_two_calls(self):
        self.mock.expect.foobar()
        self.mock.expect.barbaz()
        self.mock.object.foobar()
        self.mock.object.barbaz()
        self.mocks.tearDown()

    def test_call_not_expected_first(self):
        self.mock.expect.foobar()
        self.mock.expect.barbaz()
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mock.object.barbaz()
        self.assertEqual(str(cm.exception), "mock.barbaz called instead of mock.foobar")

    def test_call_with_arguments_not_expected_first(self):
        self.mock.expect.foobar(42)
        self.mock.expect.foobar(43)
        with self.assertRaises(MockMockMock.MockException) as cm:
            self.mock.object.foobar(43)
        self.assertEqual(str(cm.exception), "mock.foobar called with bad arguments (43,) {}")  # @todo Ask the argument checker for a description of expected arguments

    def test_many_calls(self):
        self.mock.expect.foobar(1)
        self.mock.expect.foobar(2)
        self.mock.expect.foobar(3)
        self.mock.expect.foobar(4)
        self.mock.expect.foobar(5)
        self.mock.expect.foobar(6)
        self.mock.object.foobar(1)
        self.mock.object.foobar(2)
        self.mock.object.foobar(3)
        self.mock.object.foobar(4)
        self.mock.object.foobar(5)
        self.mock.object.foobar(6)
        self.mocks.tearDown()
