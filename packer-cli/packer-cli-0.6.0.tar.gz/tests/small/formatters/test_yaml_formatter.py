#!/usr/bin/env python

"""
Tests for the YAML formatter
"""

import io
import typing
import unittest

import yaml

import packer.errors
import packer.formatters

class TestYAMLFormatter(unittest.TestCase):
    """
    Tests for the YAML formatter
    """

    def test_parse(self):
        """
        Tests that a stream can be parsed for data
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.YAMLFormatter(io_stream)

        self.assertEqual(
            data,
            formatter.data,
            'The data was parsed correctly',
        )

    def test_parse_malformed(self):
        """
        Tests that malformed data results in an error
        """

        io_stream = self._prepare_stream(':')

        with self.assertRaises(packer.errors.PackerMalformedDataError):
            packer.formatters.YAMLFormatter(io_stream)

    def test_format_pretty(self):
        """
        Tests that data can be pretty printed
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.YAMLFormatter(io_stream)

        self.assertEqual(
            yaml.dump(data, indent=4, default_flow_style=False),
            formatter.format_pretty(),
            'Data was pretty printed correctly',
        )

    def test_format_compact(self):
        """
        Tests that data can be compressed
        """

        data = {'key': 'value'}
        io_stream = self._prepare_stream(data)

        formatter = packer.formatters.YAMLFormatter(io_stream)

        self.assertEqual(
            yaml.dump(data),
            formatter.format_compact(),
            'Data was output compactly',
        )

    @staticmethod
    def _prepare_stream(data: typing.Any) -> typing.IO[typing.Any]:
        if isinstance(data, str):
            return io.BytesIO(data.encode('utf-8'))
        else:
            return io.BytesIO(yaml.dump(data).encode('utf-8'))
