"""
Tests for the base formatter implementation
"""

import typing
import unittest

import packer.errors
import packer.formatters

class TestFormatter(unittest.TestCase):
    """
    Tests for the base formatter implementation
    """

    def test_register_hook(self):
        """
        Tests that formatters are automagically registered
        """

        self.assertIn(
            'json',
            packer.formatters.Formatter.formatters,
            'json key exists in formatter registry',
        )

        self.assertEqual(
            packer.formatters.JSONFormatter,
            packer.formatters.Formatter.formatters['json'],
            'JSONFormatter was registered correctly',
        )

    def test_missing_format_name(self):
        """
        Tests that the format_name attribute is required for formatters
        """

        with self.assertRaises(packer.errors.PackerError):
            class _BadFormatter(packer.formatters.Formatter):
                def format_pretty(self) -> str:
                    return 'bad'

                def format_compact(self) -> str:
                    return 'bad'

                def parse(self, _) -> typing.Any:
                    return 'bad'

    def test_get_format_class(self):
        """
        Tests that the get_formatter_class method can get a formatter type
        """

        formatter_class = packer.formatters.Formatter.get_formatter_class('json')

        self.assertEqual(
            packer.formatters.JSONFormatter,
            formatter_class,
            'The correct formatter class was returned',
        )

    def test_get_format_class_unknown(self):
        """
        Tests that the get_formatter_class method raises an error for a bad type
        """

        with self.assertRaises(packer.errors.PackerUnknownFormatType):
            packer.formatters.Formatter.get_formatter_class('unknown')
