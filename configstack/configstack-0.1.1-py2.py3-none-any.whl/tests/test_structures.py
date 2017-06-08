# configstack/tests/test_structures.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit tests for module `structures`. """

import collections.abc
import os
import unittest

import testscenarios

from .. import structures


class module_all_TestCase(unittest.TestCase):
    """ Test cases for module attribute `__all__`. """

    def test_contains_expected_names(self):
        """ Should contain expected attribute names. """
        expected_names = [
                name for (name, value) in vars(structures).items()
                if (
                        isinstance(value, type)
                        and (
                            issubclass(value, structures.ConfigSection)
                            )
                )]
        self.assertEqual(
                sorted(structures.__all__),
                sorted(expected_names))


def setup_section_instance(testcase, section_class):
    """ Set up a test instance of `section_class` for the `testcase`. """
    testcase.test_instance = section_class(**testcase.test_instance_args)


class ConfigSection_BaseTestCase(unittest.TestCase):
    """ Base for test cases for class `ConfigSection`. """

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        if not hasattr(self, 'test_instance_args'):
            self.test_instance_args = {
                    'name': "expedita",
                    'options': {
                        'lorem': object(),
                        'ipsum': object(),
                        },
                    }
        setup_section_instance(self, structures.ConfigSection)


class ConfigSection_TestCase(ConfigSection_BaseTestCase):
    """ Test cases for class `ConfigSection`. """

    def test_instantiate(self):
        """ Should return an instance of `ConfigSection`. """
        self.assertIsInstance(self.test_instance, structures.ConfigSection)

    def test_is_instance_of_mutablemapping(self):
        """
        Should return an instance of `MutableMapping` abstract base class.
        """
        self.assertIsInstance(
                self.test_instance, collections.abc.MutableMapping)

    def test_has_empty_options(self):
        """ Should have empty `options` mapping by default. """
        if 'options' in self.test_instance_args:
            del self.test_instance_args['options']
        setup_section_instance(self, structures.ConfigSection)
        self.assertEqual(self.test_instance.options(), {})

    def test_has_specified_options(self):
        """ Should have the specified `options` mapping. """
        test_options = {'commodi': "doloribus", 'voluptate': "blanditiis"}
        self.test_instance_args['options'] = test_options
        setup_section_instance(self, structures.ConfigSection)
        self.assertEqual(self.test_instance.options(), test_options)

    def test_repr_contains_class_name(self):
        """ Programmer text representation should contain class name. """
        result = repr(self.test_instance)
        self.assertIn(type(self.test_instance).__name__, result)

    def test_repr_contains_section_name(self):
        """ Programmer text representation should contain section name. """
        result = repr(self.test_instance)
        self.assertIn(self.test_instance.name, result)

    def test_repr_contains_option_keys(self):
        """ Programmer text representation should contain option keys. """
        result = repr(self.test_instance)
        expected_keys = sorted(list(self.test_instance.keys()))
        expected_text = ", ".join(expected_keys)
        self.assertIn(expected_text, result)

    def test_str_contains_class_name(self):
        """ Text representation should contain class name. """
        result = str(self.test_instance)
        self.assertIn(type(self.test_instance).__name__, result)

    def test_str_contains_section_name(self):
        """ Text representation should contain section name. """
        result = str(self.test_instance)
        self.assertIn(self.test_instance.name, result)

    def test_str_contains_option_keys(self):
        """ Text representation should contain option keys. """
        result = str(self.test_instance)
        expected_keys = sorted(list(self.test_instance.keys()))
        expected_text = ", ".join(expected_keys)
        self.assertIn(expected_text, result)


class ConfigSection_comparison_TestCase(
        testscenarios.WithScenarios,
        ConfigSection_BaseTestCase):
    """ Test cases for comparison behaviour of `ConfigSection`. """

    _section_dolor_option_a = structures.ConfigSection(
            name='dolor', options={'a': 1})
    _section_dolor_option_n = structures.ConfigSection(
            name='dolor', options={'n': 1})
    _section_dolor_option_z = structures.ConfigSection(
            name='dolor', options={'z': 1})
    _section_rerum_option_a = structures.ConfigSection(
            name='rerum', options={'a': 1})
    _section_rerum_option_n = structures.ConfigSection(
            name='rerum', options={'n': 1})
    _section_rerum_option_z = structures.ConfigSection(
            name='rerum', options={'z': 1})
    _section_velit_option_a = structures.ConfigSection(
            name='velit', options={'a': 1})
    _section_velit_option_n = structures.ConfigSection(
            name='velit', options={'n': 1})
    _section_velit_option_z = structures.ConfigSection(
            name='velit', options={'z': 1})

    scenarios = [
            ('name-equal items-equal', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_rerum_option_n,
                'expected_lt_result': False,
                'expected_eq_result': True,
                'expected_ge_result': True,
                }),
            ('name-equal items-lesser', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_rerum_option_z,
                'expected_lt_result': True,
                'expected_eq_result': False,
                'expected_ge_result': False,
                }),
            ('name-equal items-greater', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_rerum_option_a,
                'expected_lt_result': False,
                'expected_eq_result': False,
                'expected_ge_result': True,
                }),
            ('name-lesser items-equal', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_velit_option_n,
                'expected_lt_result': True,
                'expected_eq_result': False,
                'expected_ge_result': False,
                }),
            ('name-lesser items-lesser', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_velit_option_z,
                'expected_lt_result': True,
                'expected_eq_result': False,
                'expected_ge_result': False,
                }),
            ('name-lesser items-greater', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_velit_option_a,
                'expected_lt_result': True,
                'expected_eq_result': False,
                'expected_ge_result': False,
                }),
            ('name-greater items-equal', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_dolor_option_n,
                'expected_lt_result': False,
                'expected_eq_result': False,
                'expected_ge_result': True,
                }),
            ('name-greater items-lesser', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_dolor_option_z,
                'expected_lt_result': False,
                'expected_eq_result': False,
                'expected_ge_result': True,
                }),
            ('name-greater items-greater', {
                'this_section': _section_rerum_option_n,
                'other_section': _section_dolor_option_a,
                'expected_lt_result': False,
                'expected_eq_result': False,
                'expected_ge_result': True,
                }),
            ]

    def test_lt_returns_expected_result(self):
        """ Should return expected result from `this` < `other`. """
        result = (self.this_section < self.other_section)
        self.assertEqual(result, self.expected_lt_result)

    def test_eq_returns_expected_result(self):
        """ Should return expected result from `this` == `other`. """
        result = (self.this_section == self.other_section)
        self.assertEqual(result, self.expected_eq_result)


class ConfigSection_mapping_TestCase(ConfigSection_BaseTestCase):
    """ Test cases for mapping behaviour of `ConfigSection`. """

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.test_options = {
                'lorem': object(),
                'ipsum': object(),
                }
        self.test_instance_args = {
                'name': "consecteur",
                'options': self.test_options,
                }
        super().setUp()

    def test_has_specified_name(self):
        """ Should have the specified `name`. """
        expected_name = self.test_instance_args['name']
        self.assertEqual(self.test_instance.name, expected_name)

    def test_init_sets_options_empty_by_default(self):
        """ Should have empty options dict after init. """
        del self.test_instance_args['options']
        setup_section_instance(self, structures.ConfigSection)
        expected_options = {}
        self.assertEqual(self.test_instance.options(), expected_options)

    def test_init_sets_options_to_specified_dict(self):
        """ Should have options set to specified dictionary. """
        expected_options = self.test_options
        self.assertEqual(self.test_instance.options(), expected_options)

    def test_getitem_returns_specified_option_value(self):
        """ Getitem syntax should return value for specified option. """
        test_option_name = 'lorem'
        expected_value = self.test_options[test_option_name]
        self.assertEqual(self.test_instance[test_option_name], expected_value)

    def test_setitem_sets_specified_value_in_options(self):
        """ Setitem syntax should set specified value in options. """
        test_option_name = 'lorem'
        test_option_value = object()
        expected_value = test_option_value
        self.test_instance[test_option_name] = test_option_value
        self.assertEqual(
                self.test_instance.options()[test_option_name], expected_value)

    def test_delitem_removes_specified_value_from_options(self):
        """ Delitem syntax should remove specified value from options. """
        test_option_name = 'lorem'
        del self.test_instance[test_option_name]
        self.assertFalse(test_option_name in self.test_instance.options())

    def test_iter_produces_option_names(self):
        """ Iterator syntax should produce option names. """
        names = [name for name in self.test_instance]
        expected_names = list(self.test_options.keys())
        self.assertEqual(names, expected_names)

    def test_length_returns_options_collection_length(self):
        """ Length syntax should return length of options collection. """
        expected_length = len(self.test_options)
        self.assertEqual(len(self.test_instance), expected_length)


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
