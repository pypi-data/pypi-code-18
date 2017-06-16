#!/usr/bin/env python

"""
Tests for the YAML formatter command
"""

import tempfile
import unittest.mock

import yaml

import packer.cli

from .base import CliTestCase


class TestYamlCommand(CliTestCase):
    """
    Tests for the YAML Packer command
    """

    @unittest.mock.patch('click.secho')
    def test_malformed(self, mock_secho: unittest.mock.Mock):
        """
        Tests that malformed data is failed
        """

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['yaml'],
            input=':',
        )

        self.assert_exit_equals(1, result, 'Command terminated correctly')

        mock_secho.assert_called_once_with(
            'Malformed data given',
            err=True,
            fg='red',
        )

    def test_pretty(self):
        """
        Tests that output is pretty printed correctly
        """

        data = {'key': 'value'}

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['yaml'],
            input=yaml.dump(data),
        )

        self.assert_exit_success(result, 'Command exited correctly')

        self.assertEqual(
            yaml.dump(data, indent=4, default_flow_style=False) + '\n',
            result.output,
            'YAML was pretty printed correctly',
        )

    def test_minimize(self):
        """
        Tests that output is minimized correctly
        """

        data = {'key': 'value'}

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['yaml', '--action', 'minimize'],
            input=yaml.dump(data, indent=4, default_flow_style=False),
        )

        self.assert_exit_success(result, 'Command exited correctly')

        self.assertEqual(
            yaml.dump(data) + '\n',
            result.output,
            'YAML was pretty printed correctly',
        )

    def test_source_stdin(self):
        """
        Tests that stdin can be specified as an input source
        """

        data = {'key': 'value'}

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['yaml', '--source', '-'],
            input=yaml.dump(data),
        )

        self.assert_exit_success(result, 'Command exited correctly')

        self.assertEqual(
            yaml.dump(data, indent=4, default_flow_style=False) + '\n',
            result.output,
            'YAML was retrieved correctly',
        )

    def test_source_file(self):
        """
        Tests that a file can be specified as an input source
        """

        with tempfile.NamedTemporaryFile() as source_file:
            data = {'key': 'value'}

            with open(source_file.name, 'w') as file_handle:
                yaml.dump(data, file_handle)

            result = self.cli_runner.invoke(
                packer.cli.packer_cli,
                ['yaml', '--source', source_file.name],
            )

            self.assert_exit_success(result, 'Command exited correctly')

            self.assertEqual(
                yaml.dump(data, indent=4, default_flow_style=False) + '\n',
                result.output,
                'YAML was retrieved correctly',
            )

    @unittest.mock.patch('click.secho')
    def test_validate(self, mock_secho):
        """
        Tests that the validate action only prints that the data is valid
        """

        data = {'key': 'value'}

        result = self.cli_runner.invoke(
            packer.cli.packer_cli,
            ['yaml', '--action', 'validate'],
            input=yaml.dump(data),
        )

        self.assert_exit_success(result, 'Command exited correctly')

        mock_secho.assert_called_once_with(
            'Data is valid!',
            fg='green',
        )
