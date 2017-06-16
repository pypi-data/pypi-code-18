#!/usr/bin/env python

"""
Tests for the convert command
"""

import json
import tempfile
import typing
import unittest.mock

import yaml

import packer.cli

from .base import CliTestCase


class TestConvert(CliTestCase):
    """
    Tests for the convert command
    """

    def test_malformed_data(self):
        """
        Tests that malformed data is caught
        """

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['convert', 'json', 'yaml'],
            input='{',
        )

        self.assert_exit_equals(
            1,
            result,
            'Command terminated correctly',
        )

    def test_converted(self):
        """
        Tests that the data is converted into the requested format
        """

        data = {'key': 'value'}

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['convert', 'json', 'yaml'],
            input=json.dumps(data),
        )

        self.assert_exit_success(result, 'command exited correctly')

        self.assertEqual(
            yaml.dump(data, indent=4, default_flow_style=False) + '\n',
            result.output,
            'Data was converted to YAML',
        )
