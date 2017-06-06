# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import MockMockMock


class TestException(Exception):
    pass


class SingleExpectationTestCase(MockMockMock.TestCase):
    def setUp(self):
        super(SingleExpectationTestCase, self).setUp()
        self.mock = self.mocks.create("mock")

    def test_method_call(self):
        self.mock.expect.foobar()
        self.mock.object.foobar()

    def test_method_call_with_simple_argument(self):
        self.mock.expect.foobar(42)
        self.mock.object.foobar(42)

    def test_method_call_with_return(self):
        returnValue = object()
        self.mock.expect.foobar().and_return(returnValue)
        self.assertIs(self.mock.object.foobar(), returnValue)

    def test_property_with_return(self):
        self.mock.expect.foobar.and_return(42)
        self.assertEqual(self.mock.object.foobar, 42)

    def test_object_call_with_arguments_and_return(self):
        self.mock.expect(43, 44).and_return(42)
        self.assertEqual(self.mock.object(43, 44), 42)

    def test_object_call_with_custom_arguments_checker(self):
        # See the hack in AnyAttribute.__getattr__
        self.mock.expect._call_.with_arguments(lambda args, kwds: True).and_return(42)
        self.assertEqual(self.mock.object(43, 44), 42)

    def test_method_call_with_raise(self):
        self.mock.expect.foobar().and_raise(TestException())
        with self.assertRaises(TestException):
            self.mock.object.foobar()

    def test_property_with_raise(self):
        self.mock.expect.foobar.and_raise(TestException())
        with self.assertRaises(TestException):
            self.mock.object.foobar

    def test_method_call_with_specific_action(self):
        self.check = False

        def f():
            self.check = True

        self.mock.expect.foobar().and_execute(f)
        self.mock.object.foobar()
        self.assertTrue(self.check)

    def test_property_with_specific_action(self):
        self.check = False

        def f():
            self.check = True

        self.mock.expect.foobar.and_execute(f)
        self.mock.object.foobar
        self.assertTrue(self.check)
