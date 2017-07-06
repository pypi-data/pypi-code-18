#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.flows.cisco_asa_enable_snmp_flow import CiscoEnableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV2Parameters


class TestCiscoASAEnableSNMPFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestCiscoASAEnableSNMPFlow, self).setUp()
        self.tested_instance = CiscoEnableSnmpFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestCiscoASAEnableSNMPFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_enable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success_already_configured(self, snmp_actions_class):
        """ SNMP Community already configured """

        test_snmp_community = "snmp_community"

        snmp_parameters = SNMPV2Parameters(ip="127.0.0.1", snmp_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions
        snmp_actions.get_current_snmp_communities.return_value = "some information about already configured communities"

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.get_current_snmp_communities.assert_called_once()
        snmp_actions.enable_snmp.assert_called_once_with(test_snmp_community)

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_enable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success(self, snmp_actions_class):
        """ Unsupported SNMP Version """

        test_snmp_community = "snmp_community"

        snmp_parameters = SNMPV2Parameters(ip="127.0.0.1", snmp_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions
        snmp_actions.get_current_snmp_communities.return_value = test_snmp_community

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.get_current_snmp_communities.assert_called_once()
        snmp_actions.enable_snmp.assert_not_called()

    def test_execute_flow_fail_unsupported_version(self):
        """ Unsupported SNMP Version """

        snmp_parameters = "Some SNMP Parameters structure"

        with self.assertRaisesRegexp(Exception, "Unsupported SNMP version"):
            self.tested_instance.execute_flow(snmp_parameters)

    def test_execute_flow_fail_empty_snmp_community(self):
        """ SNMP Community should not be empty """

        snmp_parameters = SNMPV2Parameters(ip="127.0.0.1", snmp_community="")

        with self.assertRaisesRegexp(Exception, "SNMP community cannot be empty"):
            self.tested_instance.execute_flow(snmp_parameters)
