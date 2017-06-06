# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import collections
import unittest

import MockMockMock


def is_callable(x):
    return isinstance(x, collections.Callable)


class PublicInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        super(PublicInterfaceTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.mock = self.mocks.create("mock")

    # No tearDown, because we really don't want to check that expectations were called

    def test_engine(self):
        self.assertEqual(
            self.dir(self.mocks),
            [
                "alternative",
                "atomic",
                "create",
                "optional",
                "ordered",
                "records",
                "repeated",
                "replace",
                "tearDown",
                "tear_down",
                "unordered",
            ]
        )
        self.assertFalse(is_callable(self.mocks))

    def test_mock(self):
        self.assertEqual(self.mock.__class__, MockMockMock.Mock)
        self.assertEqual(self.dir(self.mock), ["expect", "object", "record"])
        self.assertFalse(is_callable(self.mock))

    def test_expect(self):
        self.assertEqual(self.dir(self.mock.expect), [])
        self.assertTrue(is_callable(self.mock.expect))

    def test_expectation(self):
        self.assertEqual(self.dir(self.mock.expect.foobar), ["and_execute", "and_raise", "and_return", "with_arguments"])
        self.assertTrue(is_callable(self.mock.expect.foobar))

    def test_called_expectation(self):
        self.assertEqual(self.dir(self.mock.expect.foobar(42)), ["and_execute", "and_raise", "and_return"])
        self.assertFalse(is_callable(self.mock.expect.foobar(42)))
        self.assertEqual(self.dir(self.mock.expect.foobar.with_arguments(42)), ["and_execute", "and_raise", "and_return"])
        self.assertFalse(is_callable(self.mock.expect.foobar.with_arguments(42)))

    def test_called_then_anded_expectation(self):
        self.assertEqual(self.dir(self.mock.expect.foobar(42).and_return(12)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar(42).and_return(12)))
        self.assertEqual(self.dir(self.mock.expect.foobar(42).and_raise(None)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar(42).and_raise(None)))
        self.assertEqual(self.dir(self.mock.expect.foobar(42).and_execute(None)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar(42).and_execute(None)))

    def test_anded_expectation(self):
        self.assertEqual(self.dir(self.mock.expect.foobar.and_return(12)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar.and_return(12)))
        self.assertEqual(self.dir(self.mock.expect.foobar.and_raise(None)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar.and_raise(None)))
        self.assertEqual(self.dir(self.mock.expect.foobar.and_execute(None)), [])
        self.assertFalse(is_callable(self.mock.expect.foobar.and_execute(None)))

    def test_object(self):
        # @todo Expose expected calls in mock.object.__dir__. And check is_callable matches what's been expected. Even for an attribute that's first expected to not be called, then expected to be called: the object's corresponding attribute should show that behavior.
        self.assertEqual(self.dir(self.mock.object), [])

    def dir(self, o):
        return sorted(a for a in dir(o) if not a.startswith("_"))
