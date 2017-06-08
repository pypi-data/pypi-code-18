# configstack/tests/test_sources.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit tests for module `sources`. """

import argparse
import configparser
import functools
import io
import os
import re
import sys
import textwrap
import unittest

import testscenarios

from .. import sources
from .. import structures


class module_all_TestCase(unittest.TestCase):
    """ Test cases for module attribute `__all__`. """

    def test_contains_expected_names(self):
        """ Should contain expected attribute names. """
        expected_names = [
                name for (name, value) in vars(sources).items()
                if (
                        isinstance(value, type)
                        and (
                            issubclass(value, sources.ConfigSource)
                            )
                )]
        self.assertEqual(
                sorted(sources.__all__),
                sorted(expected_names))


class FakeConfigSource(sources.ConfigSource):
    """ Fake subclass of `ConfigSource`. """

    def sections(self):
        pass


def setup_configsource_fixture(testcase):
    """ Set up the `ConfigSource` fixture for `testcase`. """
    test_class = testcase.configsource_class
    testcase.test_configsource_instance = test_class(
            **testcase.test_configsource_args)


def add_configsection_typeequalityfunction(testcase):
    """ Add a type equality function for `ConfigSection`. """

    def assertConfigSectionEqual(testcase, first, second, msg=None):
        """
        Assert that `ConfigSection` values `first` and `second` are equal.
        """
        if not (first.options() == second.options()):
            raise testcase.failureException(msg)

    testcase.addTypeEqualityFunc(
            structures.ConfigSection,
            functools.partial(assertConfigSectionEqual, testcase))


class ConfigSource_BaseTestCase(unittest.TestCase):
    """ Base for test cases for `ConfigSource` and derived classes. """

    configsource_class = FakeConfigSource

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        add_configsection_typeequalityfunction(self)

        self.setup_test_configsource_args()
        setup_configsource_fixture(self)
        self.setup_expected_sections()

    def setup_test_configsource_args(self):
        self.test_configsource_args = {}

    def setup_expected_sections(self):
        self.expected_sections = NotImplemented

    def test_instantiate(self):
        """ Should return an instance of the test class. """
        self.assertIsInstance(
                self.test_configsource_instance, self.configsource_class)

    def test_sections_is_callable(self):
        """ Method `sections` should be callable. """
        self.assertTrue(callable(self.test_configsource_instance.sections))


class ConfigSource_TestCase(ConfigSource_BaseTestCase):
    """ Test cases for class `ConfigSource`. """

    configsource_class = FakeConfigSource

    def test_instantiate(self):
        """ Should raise TypeError when attempting to instantiate. """
        with self.assertRaises(TypeError):
            sources.ConfigSource(**self.test_configsource_args)

    def test_repr_contains_class_name(self):
        """ Programmer text representation should contain class name. """
        result = repr(self.test_configsource_instance)
        self.assertIn(type(self.test_configsource_instance).__name__, result)

    def test_str_contains_class_name(self):
        """ Text representation should contain class name. """
        result = str(self.test_configsource_instance)
        self.assertIn(type(self.test_configsource_instance).__name__, result)


def make_test_configsections():
    """ Make a collection of test `ConfigSection` instances. """
    sections = {
            'tempore': structures.ConfigSection(
                name='tempore',
                options={
                    'quibusdam': None,
                    'saepe': "necessitatibus",
                    'odit': 17,
                    },
                ),
            'nisi': structures.ConfigSection(
                name='nisi',
                options={},
                ),
            'doloribus': structures.ConfigSection(
                name='doloribus',
                options={
                    'doloremque': True,
                    },
                ),
            }
    return sections


class DefaultConfigSource_TestCase(ConfigSource_BaseTestCase):
    """ Test cases for class `DefaultConfigSource`. """

    configsource_class = sources.DefaultConfigSource

    def setup_test_configsource_args(self):
        self.test_configsections = make_test_configsections()
        self.test_configsource_args = {
                'sections': self.test_configsections,
                }

    def setup_expected_sections(self):
        """ Set up the expected sections to be set from `populate`. """
        self.expected_sections = self.test_configsections

    def test_sections_returns_expected_sections(self):
        """ Method `sections` should return expected collection. """
        result = self.test_configsource_instance.sections()
        self.assertEqual(result, self.expected_sections)


class DefaultConfigSource_from_dict_TestCase(unittest.TestCase):
    """ Test cases for method `DefaultConfigSource.from_dict`. """

    configsource_class = sources.DefaultConfigSource

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        add_configsection_typeequalityfunction(self)

        test_configsections = make_test_configsections()
        self.setup_test_from_dict_args(test_configsections)
        self.expected_sections = test_configsections

    def setup_test_configsource_args(self):
        self.test_configsource_args = {}

    def setup_test_from_dict_args(self, configsections):
        test_section_dicts = {
            name: section.options()
            for (name, section) in configsections.items()}
        self.test_from_dict_args = {
                'sections': test_section_dicts,
                }

    def setup_expected_sections(self):
        self.expected_sections = self.test_configsections

    def test_returns_expected_configsource(self):
        """ Should return expected `DefaultConfigSource` instance. """
        result = sources.DefaultConfigSource.from_dict(
                **self.test_from_dict_args)
        self.assertEqual(result.sections(), self.expected_sections)


class EnvironmentConfigSource_TestCase(ConfigSource_BaseTestCase):
    """ Test cases for class `EnvironmentConfigSource`. """

    configsource_class = sources.EnvironmentConfigSource

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.test_program_name = "deleniti"

        super().setUp()

        self.patch_os_environ()

    def setup_test_configsource_args(self):
        self.test_configsource_args = {
                'program_name': self.test_program_name,
                }

    def patch_os_environ(self):
        """ Patch the `os.environ` mapping during this test case. """
        fake_variables = {
                'DELENITI_TEMPORE_SAEPE': "necessitatibus",
                'DELENITI_TEMPORE_ODIT': "17",
                'DELENITI_NISI_CONSECTETUR_REPELLENDUS': "debitis",
                'DELENITI_NISI_EX_5_MINIMA': "42",
                'DELENITI_DOLORIBUS_DOLOREMQUE': "true",
                }
        attribute_patcher = unittest.mock.patch.object(
                os, 'environ',
                new=fake_variables)
        self.mock_os_environ = attribute_patcher.start()
        self.addCleanup(attribute_patcher.stop)

    def setup_expected_sections(self):
        """ Set up the expected sections to be set from `populate`. """
        self.expected_sections = {
                'tempore': structures.ConfigSection(
                    name='tempore',
                    options={
                        'saepe': "necessitatibus",
                        'odit': "17",
                        },
                    ),
                'nisi': structures.ConfigSection(
                    name='nisi',
                    options={
                        'consectetur_repellendus': "debitis",
                        'ex_5_minima': "42",
                        },
                    ),
                'doloribus': structures.ConfigSection(
                    name='doloribus',
                    options={
                        'doloremque': "true",
                        },
                    ),
                }

    def test_has_specified_program_name(self):
        """ Should have specified `program_name` attribute. """
        expected_program_name = self.test_program_name
        self.assertEqual(
                self.test_configsource_instance.program_name,
                expected_program_name)

    def test_sections_returns_expected_sections(self):
        """ Method `sections` should return expected collection. """
        result = self.test_configsource_instance.sections()
        self.assertEqual(result, self.expected_sections)


class ConfigParserConfigSource_TestCase(ConfigSource_BaseTestCase):
    """ Test cases for class `ConfigParserConfigSource`. """

    configsource_class = sources.ConfigParserConfigSource

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.setup_configfiles()
        self.setup_configparser_instance(self.fake_config_filenames)

        self.setup_mock_open(self.fake_config_files)

        super().setUp()

    def setup_configfiles(self):
        """ Set up the config files for this test case. """
        self.fake_config_files = {
                'lorem.conf': io.StringIO(textwrap.dedent("""\
                    [tempore]
                    odit = 17
                    [nisi]
                    ex_5_minima = 42
                    """)),
                'ipsum.conf': io.StringIO(textwrap.dedent("""\
                    [tempore]
                    saepe = necessitatibus
                    [nisi]
                    consectetur_repellendus': debitis
                    [doloribus]
                    doloremque = true
                    """)),
                }
        self.fake_config_filenames = self.fake_config_files.keys()

    def setup_configparser_instance(self, filenames):
        """ Set up the `ConfigParser` instance for this test case. """
        self.test_configparser_instance = configparser.ConfigParser()

    def setup_test_configsource_args(self):
        self.test_configsource_args = {
                'filenames': self.fake_config_filenames,
                'parser': self.test_configparser_instance,
                }

    def setup_expected_sections(self):
        """ Set up the expected sections to be set from `populate`. """
        self.expected_sections = {
                'tempore': structures.ConfigSection(
                    name='tempore',
                    options={
                        'saepe': "necessitatibus",
                        'odit': "17",
                        },
                    ),
                'nisi': structures.ConfigSection(
                    name='nisi',
                    options={
                        'consectetur_repellendus': "debitis",
                        'ex_5_minima': "42",
                        },
                    ),
                'doloribus': structures.ConfigSection(
                    name='doloribus',
                    options={
                        'doloremque': "true",
                        },
                    ),
                }

    def setup_mock_open(self, fake_files):
        """ Set up a mock for built-in `open` to return `fake_files`. """
        mock_open = unittest.mock.mock_open()
        mock_open.side_effect = self.fake_config_files.values()
        self.builtin_open_patcher = unittest.mock.patch.object(
                configparser, 'open', new=mock_open)

    def test_sections_calls_specified_parser_with_filenames(self):
        """
        Method `sections` should call specified parser `read` with filenames.
        """
        with self.builtin_open_patcher as mock_open:
            with unittest.mock.patch.object(
                    self.test_configparser_instance, 'read',
            ) as mock_parser_read:
                self.test_configsource_instance.sections()
        mock_parser_read.assert_called_with(
                filenames=self.fake_config_filenames)

    def test_sections_calls_default_parser_with_filenames(self):
        """
        Method `sections` should call default parser `read` with filenames.
        """
        del self.test_configsource_args['parser']
        with unittest.mock.patch.object(
                configparser, 'ConfigParser') as mock_configparser_class:
            setup_configsource_fixture(self)
        with self.builtin_open_patcher as mock_open:
            self.test_configsource_instance.sections()
        mock_configparser = mock_configparser_class.return_value
        mock_configparser.read.assert_called_with(
                filenames=self.fake_config_filenames)

    def test_sections_returns_expected_sections(self):
        """ Method `sections` should return expected collection. """
        with self.builtin_open_patcher:
            result = self.test_configsource_instance.sections()
        for (result_section, expected_section) in zip(
                result, self.expected_sections):
            with self.subTest(expected_section=expected_section):
                self.assertEqual(result_section, expected_section)


def setup_argparse_action_instance(testcase):
    """ Set up the `argparse.Action` instance for the `testcase`. """
    testcase.test_argparse_action_instance = testcase.argparse_action_class(
            **testcase.test_argparse_action_args)


def add_argparse_namespace_typeequalityfunction(testcase):
    """ Add a type equality function for `argparse.Namespace`. """

    def assertNamespaceEqual(testcase, first, second, msg=None):
        """
        Assert that `argparse.Namespace` values `first` and `second` are equal.
        """
        if msg is None:
            msg = "{!r} != {!r}".format(first, second)
        if not (first._get_kwargs() == second._get_kwargs()):
            raise testcase.failureException(msg)

    testcase.addTypeEqualityFunc(
            argparse.Namespace,
            functools.partial(assertNamespaceEqual, testcase))


class ConfigOptionAction_BaseTestCase(unittest.TestCase):
    """ Base for test cases for class `ConfigOptionAction`. """

    argparse_action_class = type(NotImplemented)

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        add_argparse_namespace_typeequalityfunction(self)


class ConfigOptionAction_TestCase(
        testscenarios.WithScenarios,
        ConfigOptionAction_BaseTestCase):
    """ Test cases for class `ConfigOptionAction`. """

    argparse_action_class = sources.ConfigOptionAction

    scenarios = [
            ('args-full', {
                'test_argparse_action_args': {
                    'option_strings': ["-l", "--lorem"],
                    'dest': "tempore:lorem",
                    'nargs': "*",
                    'const': "sapiente",
                    'default': "accusantium",
                    'type': int,
                    'choices': {
                        "rem", "illo", "nostrum", "cupiditate"},
                    'required': False,
                    'help': "Debitis tempore sapiente accusantium quasi.",
                    'metavar': "TEMPORE_LOREM",
                    },
                'expected_action_section_name': "tempore",
                'expected_action_option_name': "lorem",
                }),
            ('args-minimal', {
                'test_argparse_action_args': {
                    'option_strings': ["-l", "--lorem"],
                    'dest': "tempore:lorem",
                    },
                'expected_action_section_name': "tempore",
                'expected_action_option_name': "lorem",
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        setup_argparse_action_instance(self)
        self.setup_expected_argparse_action()

    def setup_expected_argparse_action(self):
        """ Set expected arguments to the `argparse.Action` cosntructor. """
        expected_args = dict(self.test_argparse_action_args)
        expected_args['dest'] = self.expected_action_section_name
        action = argparse.Action(**expected_args)
        action.config_section_name = self.expected_action_section_name
        action.config_option_name = self.expected_action_option_name
        self.expected_argparse_action = action

    def test_instantiate(self):
        """ Should return an instance of the test class. """
        self.assertIsInstance(
                self.test_argparse_action_instance,
                self.argparse_action_class)

    def test_instance_matches_expected_action(self):
        """ Should return an instance matching the expected action object. """
        self.assertEqual(
                self.test_argparse_action_instance._get_kwargs(),
                self.expected_argparse_action._get_kwargs())


def setup_argumentparser_instance(testcase):
    """ Set up the `ArgumentParser` instance for the `testcase`. """
    testcase.argumentparser = argparse.ArgumentParser()
    testcase.argumentparser.add_argument("-i", "--ipsum", action='store_true')
    testcase.argumentparser.add_argument(
            "-l", "--lorem",
            dest="tempore:lorem",
            nargs=1,
            action=testcase.argparse_action_class)
    testcase.argumentparser.add_argument(
            "--consectetur",
            dest="nisi:consectetur_repellendus",
            nargs=1,
            action=testcase.argparse_action_class)
    testcase.argumentparser.add_argument(
            "nisi:ex_5_minima",
            nargs=1,
            action=testcase.argparse_action_class)


class ConfigOptionAction_call_TestCase(
        testscenarios.WithScenarios,
        ConfigOptionAction_BaseTestCase):
    """ Test cases for `ConfigOptionAction` call. """

    argparse_action_class = sources.ConfigOptionAction

    scenarios = [
            ('configoption-none', {
                'test_argv': [
                    "deleniti",
                    "--ipsum",
                    "harum",
                    ],
                'expected_namespace': argparse.Namespace(
                    ipsum=True,
                    tempore=None,
                    nisi=structures.ConfigSection(
                        name='nisi',
                        options={
                            'ex_5_minima': "harum",
                            }),
                    ),
                }),
            ('configoption-two', {
                'test_argv': [
                    "deleniti",
                    "--ipsum",
                    "--lorem", "soluta",
                    "harum",
                    ],
                'expected_namespace': argparse.Namespace(
                    ipsum=True,
                    tempore=structures.ConfigSection(
                        name='tempore',
                        options={
                            'lorem': "soluta",
                            }),
                    nisi=structures.ConfigSection(
                        name='nisi',
                        options={
                            'ex_5_minima': "harum",
                            }),
                    ),
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        setup_argumentparser_instance(self)

    def setup_test_argparse_action_args(self):
        self.test_argparse_action_args = self.action_args

    def test_returns_expected_namespace(self):
        """ Should return expected namespace collection. """
        result = self.argumentparser.parse_args(self.test_argv[1:])
        self.assertEqual(result, self.expected_namespace)


class ArgumentParserConfigSource_TestCase(ConfigSource_BaseTestCase):
    """ Test cases for class `ArgumentParserConfigSource`. """

    configsource_class = sources.ArgumentParserConfigSource
    argparse_action_class = sources.ConfigOptionAction

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.test_program_name = "deleniti"
        setup_argumentparser_instance(self)

        super().setUp()

        self.test_argv = [
                self.test_program_name,
                "--lorem", "accusantium",
                "harum",
        ]

    def setup_test_configsource_args(self):
        self.test_configsource_args = {
                'parser': self.argumentparser,
                }

    def setup_expected_sections(self):
        self.expected_sections = {
                'tempore': structures.ConfigSection(
                    name='tempore',
                    options={
                        'lorem': "accusantium",
                        },
                    ),
                'nisi': structures.ConfigSection(
                    name='nisi',
                    options={
                        'ex_5_minima': "harum",
                        },
                    ),
                }

    def test_sections_returns_expected_sections(self):
        """ Method `sections` should return expected collection. """
        with unittest.mock.patch.object(sys, 'argv', self.test_argv):
            result = self.test_configsource_instance.sections()
        self.assertEqual(result, self.expected_sections)


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
