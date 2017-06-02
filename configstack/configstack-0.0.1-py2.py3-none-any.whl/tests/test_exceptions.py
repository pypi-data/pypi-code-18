# configstack/tests/test_exceptions.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit tests for module `exceptions`. """

import unittest

import testscenarios

from .. import exceptions


class exception_TestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Test cases for exception classes. """

    scenarios = [
            ('ConfigStackException', {
                'exception_class': exceptions.ConfigStackException,
                'exception_class_args': {},
                'expected_classes': [],
                }),
            ('LayerNotPopulatedError', {
                'exception_class': exceptions.LayerNotPopulatedError,
                'exception_class_args': {},
                'expected_classes': [
                    exceptions.ConfigStackException,
                    RuntimeError,
                    ],
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.setup_exception_instance()

    def setup_exception_instance(self):
        """ Set up the test instance for this test case. """
        self.test_exception_instance = self.exception_class(
                **self.exception_class_args)

    def test_instantiate(self):
        """ Should instantiate the expected class. """
        self.assertIsInstance(
                self.test_exception_instance, self.exception_class)

    def test_is_instance_of_expected_classes(self):
        """ Should be an instance of the expected classes. """
        for expected_class in self.expected_classes:
            with self.subTest(expected_class=expected_class):
                self.assertIsInstance(
                        self.test_exception_instance, expected_class)


# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
