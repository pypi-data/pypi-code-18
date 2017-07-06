#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.cli.cli_service_impl import CliServiceImpl as CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.firewall.cisco.asa.command_templates import enable_disable_snmp


class EnableDisableSnmpActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: config mode cli service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    @property
    def client_ip_address(self):
        """ Client IP Address """

        try:
            return self._cli_service.session.get_local_address()
        except Exception, err:
            self._logger.error("Failed to determine client local IP Address: {}".format(err))
            raise Exception(self.__class__.__name__, "Failed to determine client local IP Address: {}".format(err))

    @property
    def interface_name(self):
        """ Device interface name """

        return self.get_interface_name(cli_service=self._cli_service)

    def get_current_snmp_communities(self, cli_service=None, action_map=None, error_map=None):
        """Retrieve current snmp communities

        :param cli_service:
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return:
        """

        if not cli_service:
            cli_service = self._cli_service
        output = CommandTemplateExecutor(cli_service=cli_service,
                                         command_template=enable_disable_snmp.SHOW_SNMP_COMMUNITY,
                                         action_map=action_map,
                                         error_map=error_map).execute_command()

        return re.findall(r"community (\S+) version", output, flags=re.DOTALL)

    def get_interface_name(self, cli_service=None, action_map=None, error_map=None):
        """ Get interface name

        :param cli_service:
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return:
        """

        if not cli_service:
            cli_service = self._cli_service
        output = CommandTemplateExecutor(cli_service=cli_service,
                                         command_template=enable_disable_snmp.SHOW_IP_ADDR,
                                         action_map=action_map,
                                         error_map=error_map).execute_command(ip_address=self._cli_service.session.host)

        match = re.search(r"\S+\s+(?P<iface_name>\S+)\s+{}".format(self._cli_service.session.host), output, flags=re.DOTALL)
        if match:
            iface_name = match.group("iface_name")
            if iface_name:
                return iface_name

        self._logger("Failed to determine interface name")
        raise Exception(self.__class__.__name__, "Failed to determine interface name")

    def enable_snmp(self, snmp_community, action_map=None, error_map=None):
        """Enable SNMP on the device

        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=enable_disable_snmp.ENABLE_SNMP_SERVER,
                                action_map=action_map,
                                error_map=error_map).execute_command()

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=enable_disable_snmp.ENABLE_SNMP,
                                action_map=action_map,
                                error_map=error_map).execute_command(snmp_community=snmp_community,
                                                                     iface_name=self.interface_name,
                                                                     hostname=self.client_ip_address)

    def disable_snmp(self, snmp_community, action_map=None, error_map=None):
        """Disable SNMP on the device

        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.DISABLE_SNMP,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(snmp_community=snmp_community,
                                                                            iface_name=self.interface_name,
                                                                            hostname=self.client_ip_address)
