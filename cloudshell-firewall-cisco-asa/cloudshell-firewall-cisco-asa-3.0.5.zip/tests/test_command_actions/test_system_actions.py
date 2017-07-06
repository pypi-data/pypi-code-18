#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.command_actions.system_actions import SystemActions


class TestSystemActions(unittest.TestCase):
    def setUp(self):
        cli_service = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestSystemActions, self).setUp()
        self.tested_instance = SystemActions(cli_service=cli_service, logger=logger)

    def tearDown(self):
        super(TestSystemActions, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.system_actions.CommandTemplateExecutor")
    def test_copy_success(self, executor_class):
        """ Successfully copied without using noconfirm flag """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command = mock.MagicMock(side_effect=["Copy complete"])

        self.tested_instance.copy("source", "destination", noconfirm=False)
        executor.execute_command.assert_called_once_with(src="source", dst="destination")

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.system_actions.CommandTemplateExecutor")
    def test_copy_success_noconfirm(self, executor_class):
        """ Successfully copied with using noconfirm flag """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command = mock.MagicMock(side_effect=["Copy complete"])

        self.tested_instance.copy("source", "destination")
        executor.execute_command.assert_called_once_with(src="source", dst="destination", noconfirm="")

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.system_actions.CommandTemplateExecutor")
    def test_copy_success_noconfirm_not_supported(self, executor_class):
        """ Successfully copied but noconfirm flag isn't supported """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command = mock.MagicMock(side_effect=["Invalid input detected", "Copy complete"])

        self.tested_instance.copy("source", "destination")

        self.assertEqual(executor.execute_command.call_count, 2)
        executor.execute_command.assert_any_call(src="source", dst="destination", noconfirm="")
        executor.execute_command.assert_any_call(src="source", dst="destination")

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.system_actions.CommandTemplateExecutor")
    def test_copy_failed(self, executor_class):
        """ Successfully copied without using noconfirm flag """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command = mock.MagicMock(side_effect=["Some error happens"])

        with self.assertRaisesRegexp(Exception, "Copy Command failed"):
            self.tested_instance.copy("source", "destination")
