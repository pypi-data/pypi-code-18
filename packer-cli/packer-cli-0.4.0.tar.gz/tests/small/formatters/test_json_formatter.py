"""
JSON formatter tests
"""

import io
import json
import typing
import unittest

import packer.errors
import packer.formatters

class TestJSONFormatter(unittest.TestCase):
    """
    Tests for the JSONFormatter class
    """

    def test_parse(self):
        """
        Tests that the parse method can parse the JSON data
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.JSONFormatter(io_stream)

        self.assertDictEqual(
            data,
            formatter.data,
            'Data was parsed correctly',
        )

    def test_parse_malformed(self):
        """
        Tests that the parse method throws an exception for malformed data
        """

        with self.assertRaises(packer.errors.PackerMalformedDataError):
            packer.formatters.JSONFormatter(self._prepare_stream('{'))

    def test_format_pretty(self):
        """
        Tests that the format_pretty method returns pretty printed data
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.JSONFormatter(io_stream)

        self.assertEqual(
            json.dumps(data, indent=4),
            formatter.format_pretty(),
            'Data was pretty formatted correctly',
        )

    def test_format_compact(self):
        """
        Tests that the format_compact method returns compact data
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.JSONFormatter(io_stream)

        self.assertEqual(
            json.dumps(data),
            formatter.format_compact(),
            'Data was formatted compactly',
        )

    @staticmethod
    def _prepare_stream(data: typing.Any) -> typing.IO[typing.Any]:
        if isinstance(data, str):
            return io.BytesIO(data.encode('utf-8'))

        return io.BytesIO(json.dumps(data).encode('utf-8'))
