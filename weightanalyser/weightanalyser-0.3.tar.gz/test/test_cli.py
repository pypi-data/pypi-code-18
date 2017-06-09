from __future__ import absolute_import
import unittest

import weightanalyser.cli as cli


class TestCheckDateFormat(unittest.TestCase):
    def test_check_date_format_for_letters(self):
        self.assertFalse(cli.check_date_format("a") == "Contains letter!")

    def test_check_date_format_right(self):
        self.assertTrue(cli.check_date_format("01-12-2016"))

    def test_check_date_format_wrong_format(self):
        self.assertFalse(cli.check_date_format("01--2016"))
        self.assertFalse(cli.check_date_format("01-2016"))
        self.assertFalse(cli.check_date_format("-01-2016"))
        self.assertFalse(cli.check_date_format("01-1-2016"))
        self.assertFalse(cli.check_date_format("1-01-2016"))
        self.assertFalse(cli.check_date_format("01-01-16"))


class TestCheckMassValueFormat(unittest.TestCase):
    def test_check_mass_value_format_right_format(self):
        self.assertTrue(cli.check_mass_value_format("100.0"))
        self.assertTrue(cli.check_mass_value_format("100"))
        self.assertTrue(cli.check_mass_value_format("90.0"))
        self.assertTrue(cli.check_mass_value_format("90"))

    def test_check_mass_value_format_wrong_format(self):
        self.assertFalse(cli.check_mass_value_format("a"))


class TestCheckPercentValueFormat(unittest.TestCase):
    def test_check_percent_value_format_right(self):
        self.assertTrue(cli.check_percent_value_format("33"))
        self.assertTrue(cli.check_percent_value_format("16.1"))
        self.assertTrue(cli.check_percent_value_format("9"))

    def test_check_percent_value_format_wrong(self):
        self.assertFalse(cli.check_percent_value_format("a"))
        self.assertFalse(cli.check_percent_value_format("1000"))
        self.assertFalse(cli.check_percent_value_format("1.000"))
