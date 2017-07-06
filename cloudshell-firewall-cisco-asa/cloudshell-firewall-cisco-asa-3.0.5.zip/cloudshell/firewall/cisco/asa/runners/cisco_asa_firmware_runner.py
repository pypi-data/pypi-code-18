#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.firmware_runner import FirmwareRunner
from cloudshell.firewall.cisco.asa.cli.cisco_asa_cli_handler import CiscoASACliHandler
from cloudshell.firewall.cisco.asa.flows.cisco_asa_load_firmware_flow import CiscoASALoadFirmwareFlow


class CiscoASAFirmwareRunner(FirmwareRunner):
    RELOAD_TIMEOUT = 500

    def __init__(self, cli, logger, resource_config, api):
        """Handle firmware upgrade process

        :param CLI cli: Cli object
        :param qs_logger logger: logger
        :param CloudShellAPISession api: cloudshell api object
        :param GenericNetworkingResource resource_config:
        """

        super(CiscoASAFirmwareRunner, self).__init__(logger)
        self.cli = cli
        self.api = api
        self.resource_config = resource_config

    @property
    def cli_handler(self):
        return CiscoASACliHandler(self.cli, self.resource_config, self._logger, self.api)

    @property
    def load_firmware_flow(self):
        return CiscoASALoadFirmwareFlow(self.cli_handler, self._logger)
