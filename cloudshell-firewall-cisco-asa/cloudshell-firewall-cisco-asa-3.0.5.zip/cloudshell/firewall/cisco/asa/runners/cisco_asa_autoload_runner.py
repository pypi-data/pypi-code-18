#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.autoload_runner import AutoloadRunner

from cloudshell.firewall.cisco.asa.flows.cisco_asa_autoload_flow import CiscoASASnmpAutoloadFlow
from cloudshell.firewall.cisco.asa.snmp.cisco_asa_snmp_handler import CiscoASASnmpHandler


class CiscoASAAutoloadRunner(AutoloadRunner):
    def __init__(self, cli, logger, resource_config, api):
        super(CiscoASAAutoloadRunner, self).__init__(resource_config)
        self._cli = cli
        self._api = api
        self._logger = logger

    @property
    def snmp_handler(self):
        return CiscoASASnmpHandler(self._cli, self.resource_config, self._logger, self._api)

    @property
    def autoload_flow(self):
        return CiscoASASnmpAutoloadFlow(self.snmp_handler, self._logger)
