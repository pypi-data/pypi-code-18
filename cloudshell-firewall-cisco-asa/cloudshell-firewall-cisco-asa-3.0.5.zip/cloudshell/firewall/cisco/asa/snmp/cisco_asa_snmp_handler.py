#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.firewall.cisco.asa.cli.cisco_asa_cli_handler import CiscoASACliHandler
from cloudshell.firewall.cisco.asa.flows.cisco_asa_disable_snmp_flow import CiscoDisableSnmpFlow
from cloudshell.firewall.cisco.asa.flows.cisco_asa_enable_snmp_flow import CiscoEnableSnmpFlow
from cloudshell.devices.snmp_handler import SnmpHandler


class CiscoASASnmpHandler(SnmpHandler):
    def __init__(self, cli, resource_config, logger, api):
        super(CiscoASASnmpHandler, self).__init__(resource_config, logger, api)
        self._cli = cli
        self._api = api

    @property
    def cli_handler(self):
        return CiscoASACliHandler(self._cli, self.resource_config, self._logger, self._api)

    def _create_enable_flow(self):
        return CiscoEnableSnmpFlow(self.cli_handler, self._logger)

    def _create_disable_flow(self):
        return CiscoDisableSnmpFlow(self.cli_handler, self._logger)
