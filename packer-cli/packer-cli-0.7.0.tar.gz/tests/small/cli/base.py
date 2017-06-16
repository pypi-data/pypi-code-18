"""
Utilities for testing CLI commands
"""

import typing
import unittest

import click.testing


class CliTestCase(unittest.TestCase):
    """
    TestCase mixin for working with CLI tests
    """

    def setUp(self):
        """
        Sets up the CLI runner
        """

        super().setUp()

        self.cli_runner = click.testing.CliRunner()

    def assert_exit_equals( # type: ignore
            self,
            expected: int, result: click.testing.Result,
            msg: typing.Optional[str]=None):
        """
        Assert that the exit code matches what is expected
        """

        self.assertEqual(
            expected,
            result.exit_code,
            msg=msg,
        )

    def assert_exit_success( # type: ignore
            self,
            result: click.testing.Result,
            msg: typing.Optional[str]=None):
        """
        Tests that the exit code shows a success
        """

        self.assert_exit_equals(0, result, msg=msg)
