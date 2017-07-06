#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.snmp_action_flows import AutoloadFlow
from cloudshell.firewall.cisco.asa.autoload.cisco_asa_snmp_autoload import CiscoASASNMPAutoload


class CiscoASASnmpAutoloadFlow(AutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        with self._snmp_handler.get_snmp_service() as snpm_service:
            cisco_snmp_autoload = CiscoASASNMPAutoload(snpm_service,
                                                       shell_name,
                                                       shell_type,
                                                       resource_name,
                                                       self._logger)
            return cisco_snmp_autoload.discover(supported_os)
