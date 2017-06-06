# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import os.path

import MockMockMock


class SystemCallsTestCase(unittest.TestCase):
    def setUp(self):
        super(SystemCallsTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()

    def test_mock_globally_imported_function(self):
        original = os.path.exists
        m = self.mocks.replace("os.path.exists")
        m.expect("foo").and_return(True)
        self.assertTrue(os.path.exists("foo"))
        self.mocks.tearDown()
        self.assertIs(os.path.exists, original)
        self.assertFalse(os.path.exists("foo"))

    def test_mock_locally_imported_function(self):
        import subprocess
        original = subprocess.check_output
        m = self.mocks.replace("subprocess.check_output")
        m.expect(["foo", "bar"]).and_return("baz\n")
        self.assertEqual(subprocess.check_output(["foo", "bar"]), "baz\n")
        self.mocks.tearDown()
        self.assertIs(subprocess.check_output, original)
        self.assertEqual(subprocess.check_output(["echo", "toto"]), b"toto\n")

    def test_mock_unexisting_thing(self):
        with self.assertRaises(MockMockMock.MockException) as catcher:
            self.mocks.replace("foo.bar")
        self.assertEqual(catcher.exception.args, ("Unable to replace foo.bar",))

    def test_mock_unexisting_intermediate_thing(self):
        with self.assertRaises(MockMockMock.MockException) as catcher:
            self.mocks.replace("os.foo.bar")
        self.assertEqual(catcher.exception.args, ("Unable to replace os.foo.bar",))

    def test_mock_unexisting_subthing(self):
        with self.assertRaises(MockMockMock.MockException) as catcher:
            self.mocks.replace("os.path.foobar")
        self.assertEqual(catcher.exception.args, ("Unable to replace os.path.foobar",))
