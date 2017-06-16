#!/usr/bin/env python

"""
Tests for the main CLI command group
"""

import packer.cli

from .base import CliTestCase


class TestPackerGroup(CliTestCase):
    """
    Tests for the main Packer application command group
    """

    def test_group(self):
        """
        Tests that the command group returns group help
        """

        result = self.cli_runner.invoke(packer.cli.packer_cli)

        self.assert_exit_success(result, 'Command exited correctly')

        self.assertIn(
            'json',
            result.output,
            'JSON subcommand was in the help output',
        )
