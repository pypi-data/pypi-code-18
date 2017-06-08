# configstack/tests/test_layers.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit tests for module `layers`. """

import unittest

import testscenarios

from .. import sources
from .. import layers
from .. import structures
from .test_sources import (
        FakeConfigSource,
        setup_configsource_fixture,
        )


class module_all_TestCase(unittest.TestCase):
    """ Test cases for module attribute `__all__`. """

    def test_contains_expected_names(self):
        """ Should contain expected attribute names. """
        expected_names = [
                name for (name, value) in vars(layers).items()
                if (
                        isinstance(value, type)
                        and (
                            issubclass(value, Exception)
                            or issubclass(value, layers.ConfigLayer)
                            or issubclass(value, layers.ConfigStack)
                            )
                )]
        self.assertEqual(
                sorted(layers.__all__),
                sorted(expected_names))


def setup_configlayer_fixture(testcase):
    """ Set up the `ConfigLayer` fixture for `testcase`. """
    test_class = testcase.configlayer_class
    testcase.test_configlayer_instance = test_class(
            **testcase.test_configlayer_args)


class ConfigLayer_BaseTestCase(unittest.TestCase):
    """ Base for test cases for class `ConfigLayer`. """

    configsource_class = FakeConfigSource
    configlayer_class = layers.ConfigLayer

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.setup_test_configsource_args()
        setup_configsource_fixture(self)
        self.setup_expected_sections()

        self.setup_test_configlayer_args()
        self.setup_test_populate_args()
        setup_configlayer_fixture(self)

    def setup_test_configsource_args(self):
        self.test_configsource_args = {}

    def setup_test_configlayer_args(self):
        self.test_configlayer_args = {
                'name': "rem porro",
                'source': self.test_configsource_instance,
                }

    def setup_test_configsource(self):
        self.test_configsource = NotImplemented

    def setup_expected_sections(self):
        self.expected_sections = NotImplemented

    def setup_test_populate_args(self):
        self.test_populate_args = {}

    def test_instantiate(self):
        """ Should return an instance of the test class. """
        self.assertIsInstance(
                self.test_configlayer_instance, self.configlayer_class)

    def test_has_specified_name(self):
        """ Should have specified `name`. """
        expected_name = self.test_configlayer_args['name']
        self.assertEqual(self.test_configlayer_instance.name, expected_name)

    def test_has_specified_source(self):
        """ Should have specified `source`. """
        expected_source = self.test_configlayer_args['source']
        self.assertEqual(
                self.test_configlayer_instance.source, expected_source)

    def test_populate_is_callable(self):
        """ Method `populate` should be callable. """
        self.assertTrue(callable(self.test_configlayer_instance.populate))

    def test_sections_raises_error_when_not_populated(self):
        """ Method `sections` should raise error when not populated. """
        with self.assertRaises(self.configlayer_class.NotPopulatedError):
            self.test_configlayer_instance.sections()

    def test_sections_returns_sections_from_source(self):
        """ Method `sections` should return sections from `source`. """
        self.test_configlayer_instance.populate()
        result = self.test_configlayer_instance.sections()
        expected_sections = self.test_configsource_instance.sections()
        self.assertEqual(result, expected_sections)


class ConfigLayer_TestCase(ConfigLayer_BaseTestCase):
    """ Test cases for class `ConfigLayer`. """

    def test_repr_contains_class_name(self):
        """ Programmer text representation should contain class name. """
        result = repr(self.test_configlayer_instance)
        self.assertIn(type(self.test_configlayer_instance).__name__, result)

    def test_repr_contains_layer_name(self):
        """ Programmer text representation should contain layer name. """
        result = repr(self.test_configlayer_instance)
        self.assertIn(self.test_configlayer_instance.name, result)

    def test_repr_contains_source_repr(self):
        """ Programmer text representation should contain source. """
        result = repr(self.test_configlayer_instance)
        expected_text = repr(self.test_configlayer_instance.source)
        self.assertIn(expected_text, result)

    def test_str_contains_class_name(self):
        """ Text representation should contain class name. """
        result = str(self.test_configlayer_instance)
        self.assertIn(type(self.test_configlayer_instance).__name__, result)

    def test_str_contains_layer_name(self):
        """ Text representation should contain layer name. """
        result = str(self.test_configlayer_instance)
        self.assertIn(self.test_configlayer_instance.name, result)

    def test_str_contains_source_str(self):
        """ Text representation should contain source. """
        result = str(self.test_configlayer_instance)
        expected_text = str(self.test_configlayer_instance.source)
        self.assertIn(expected_text, result)


class ConfigStack_TestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Test cases for class `ConfigStack`. """

    scenarios = [
            ('layers-one', {
                'layers_params': [
                    {
                        'name': "quaerat",
                        'fake_sections': {
                            'amet': structures.ConfigSection(
                                name="amet",
                                options={
                                    'aspernatur': "reiciendis",
                                    'quis': "tempora",
                                    },
                                ),
                            },
                        },
                    ],
                'expected_sections': {
                    'amet': structures.ConfigSection(
                        name="amet",
                        options={
                            'aspernatur': "reiciendis",
                            'quis': "tempora",
                            },
                        ),
                    },
                }),
            ('layers-three', {
                'layers_params': [
                    {
                        'name': "quaerat",
                        'fake_sections': {
                            'amet': structures.ConfigSection(
                                name="amet",
                                options={
                                    'aspernatur': "reiciendis",
                                    'quis': "tempora",
                                    },
                                ),
                            },
                        },
                    {
                        'name': "eligendi",
                        'fake_sections': {
                            'porro': structures.ConfigSection(
                                name="porro",
                                options={
                                    'rerum': "velit",
                                    },
                                ),
                            },
                        },
                    {
                        'name': "explicabo",
                        'fake_sections': {
                            'facere': structures.ConfigSection(
                                name="facere",
                                options={
                                    'nam': "consectetur",
                                    },
                                ),
                            },
                        },
                    ],
                'expected_sections': {
                    'amet': structures.ConfigSection(
                        name="amet",
                        options={
                            'aspernatur': "reiciendis",
                            'quis': "tempora",
                            },
                        ),
                    'porro': structures.ConfigSection(
                        name="porro",
                        options={
                            'rerum': "velit",
                            },
                        ),
                    'facere': structures.ConfigSection(
                        name="facere",
                        options={
                            'nam': "consectetur",
                            },
                        ),
                    },
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.setup_fake_layers()
        self.test_configstack_instance = layers.ConfigStack(
                layers=self.fake_layers)

    def setup_fake_layers(self):
        self.fake_layers = []

        for layer_params in self.layers_params:
            layer = layers.ConfigLayer(
                name=layer_params['name'],
                source=FakeConfigSource(),
            )
            layer._sections = layer_params['fake_sections']
            self.fake_layers.append(layer)

    def test_sections_aggregates_sections_from_all_layers(self):
        """ Method `sections` should aggregate sections from all layers. """
        result = self.test_configstack_instance.sections()
        for (section_name, expected_section) in self.expected_sections.items():
            with self.subTest(section_name=section_name):
                result_section = result[section_name]
                self.assertEqual(result_section, expected_section)

    def test_repr_contains_class_name(self):
        """ Programmer text representation should contain class name. """
        result = repr(self.test_configstack_instance)
        self.assertIn(type(self.test_configstack_instance).__name__, result)

    def test_repr_contains_layer_names(self):
        """ Programmer text representation should contain layer names. """
        result = repr(self.test_configstack_instance)
        for layer in self.fake_layers:
            with self.subTest(layer=layer.name):
                self.assertIn(layer.name, result)

    def test_str_contains_class_name(self):
        """ Text representation should contain class name. """
        result = str(self.test_configstack_instance)
        self.assertIn(type(self.test_configstack_instance).__name__, result)

    def test_str_contains_layer_names(self):
        """ Text representation should contain layer names. """
        result = str(self.test_configstack_instance)
        for layer in self.fake_layers:
            with self.subTest(layer=layer.name):
                self.assertIn(layer.name, result)


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
