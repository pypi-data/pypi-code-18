#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.configuration_runner import ConfigurationRunner
from cloudshell.firewall.cisco.asa.cli.cisco_asa_cli_handler import CiscoASACliHandler
from cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow import CiscoASARestoreFlow
from cloudshell.firewall.cisco.asa.flows.cisco_asa_save_flow import CiscoASASaveFlow


class CiscoASAConfigurationRunner(ConfigurationRunner):
    def __init__(self, cli, logger, resource_config, api):
        super(CiscoASAConfigurationRunner, self).__init__(logger, resource_config, api)
        self._cli = cli

    @property
    def cli_handler(self):
        """ CLI Handler property
        :return: CLI handler
        """
        return CiscoASACliHandler(self._cli, self.resource_config, self._logger, self._api)

    @property
    def restore_flow(self):
        return CiscoASARestoreFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def save_flow(self):
        return CiscoASASaveFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        return "flash:"
