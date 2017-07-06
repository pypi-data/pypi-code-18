#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.flows.cisco_asa_save_flow import CiscoASASaveFlow


class TestCiscoASASaveFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestCiscoASASaveFlow, self).setUp()
        self.tested_instance = CiscoASASaveFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestCiscoASASaveFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_save_flow.SystemActions")
    def test_execute_flow_success(self, system_actions_class):
        folder_path = mock.MagicMock()
        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()

        self.tested_instance.execute_flow(folder_path, "running")
        sys_actions.copy.assert_called_once_with("running-config", folder_path, action_map=action_map)
