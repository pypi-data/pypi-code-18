#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.command_actions.iface_actions import IFaceActions


class TestIFaceActions(unittest.TestCase):
    def setUp(self):
        cli_service = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestIFaceActions, self).setUp()
        self.tested_instance = IFaceActions(cli_service=cli_service, logger=logger)

    def tearDown(self):
        super(TestIFaceActions, self).tearDown()
        del self.tested_instance

    def test_get_port_name_empty_port_value(self):
        """ Raise Exception because port is empty or None """
        with self.assertRaisesRegexp(Exception, "Failed to get port name."):
            self.tested_instance.get_port_name(port=None)
        with self.assertRaisesRegexp(Exception, "Failed to get port name."):
            self.tested_instance.get_port_name(port="")

    def test_get_port_name_portchannel(self):
        """ Successfully return port-channel name """

        self.assertEqual(self.tested_instance.get_port_name("CH1/M1/port-channel-4"), "port-channel-4")

    def test_get_port_name_portname(self):
        """ Successfully return port name """

        self.assertEqual(self.tested_instance.get_port_name("CH1/M1/Ethernet-4"), "Ethernet/4")

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.iface_actions.CommandTemplateExecutor")
    def test_execute_flow_success(self, executor_class):

        executor = mock.MagicMock()
        executor_class.return_value = executor

        self.tested_instance.enter_iface_config_mode("port_name")
        executor.execute_command.assert_called_once_with(port_name="port_name")

    @mock.patch("cloudshell.firewall.cisco.asa.command_actions.iface_actions.CommandTemplateExecutor")
    def test_clean_interface_switchport_config(self, executor_class):
        executor = mock.MagicMock()
        executor_class.return_value = executor

        current_config = """ some config line
                             switchport config line 1
                             another config line
                             switchport config line 2
                         """

        self.tested_instance.clean_interface_switchport_config(current_config)

        self.assertEqual(executor.execute_command.call_count, 2)
        executor.execute_command.assert_any_call(command="switchport config line 1")
        executor.execute_command.assert_any_call(command="switchport config line 2")
