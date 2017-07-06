#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.flows.cisco_asa_disable_snmp_flow import CiscoDisableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV2Parameters


class TestCiscoASAEnableSNMPFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestCiscoASAEnableSNMPFlow, self).setUp()
        self.tested_instance = CiscoDisableSnmpFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestCiscoASAEnableSNMPFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success(self, snmp_actions_class):
        """ SNMP Community already configured """

        test_snmp_community = "snmp_community"

        snmp_parameters = SNMPV2Parameters(ip="127.0.0.1", snmp_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp.assert_called_once_with(test_snmp_community)

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_skip_unsupported_version(self, snmp_actions_class):
        """ Disable SNMP Read Community skipped. Unsupported SNMP Version """

        snmp_parameters = "Some SNMP Parameters structure"
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp.assert_not_called()

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_skip_empty_community(self, snmp_actions_class):
        """ Disable SNMP Read Community skipped. SNMP Read Community is Empty """

        snmp_parameters = SNMPV2Parameters(ip="127.0.0.1", snmp_community="")
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp.assert_not_called()
