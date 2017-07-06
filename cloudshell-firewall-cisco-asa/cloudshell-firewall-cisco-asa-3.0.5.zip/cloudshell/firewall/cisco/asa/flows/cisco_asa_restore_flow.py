#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.action_flows import RestoreConfigurationFlow
from cloudshell.firewall.cisco.asa.command_actions.system_actions import SystemActions
from cloudshell.cli.session.session_exceptions import ExpectedSessionException


class CiscoASARestoreFlow(RestoreConfigurationFlow):
    SESSION_RECONNECT_TIMEOUT = 300
    BACKUP_STARTUP = "flash:backup-sc"

    def __init__(self, cli_handler, logger):
        super(CiscoASARestoreFlow, self).__init__(cli_handler, logger)

    def execute_flow(self, path, configuration_type, restore_method, vrf_management_name=None):
        """ Execute flow which save selected file to the provided destination

        :param path: the path to the configuration file, including the configuration file name
        :param restore_method: the restore method to use when restoring the configuration file.
                               Possible Values are append and override
        :param configuration_type: the configuration type to restore. Possible values are startup and running
        :param vrf_management_name: Virtual Routing and Forwarding Name
        """

        configuration_type = "{}-config".format(configuration_type)

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            restore_action = SystemActions(enable_session, self._logger)
            copy_action_map = restore_action.prepare_action_map(path, configuration_type)

            if configuration_type == "startup-config" and restore_method == "append":
                raise Exception(self.__class__.__name__,
                                "Restore 'startup-config' with method 'append' is not supported")
            elif configuration_type == "startup-config" and restore_method == "override":
                restore_action.copy(path, configuration_type, action_map=copy_action_map)
            elif configuration_type == "running-config" and restore_method == "override":
                self._logger.debug("Start backup process for 'startup-config' config")
                try:
                    restore_action.copy("startup-config", self.BACKUP_STARTUP, action_map=copy_action_map)
                except:
                    raise Exception(self.__class__.__name__,
                                    "Failed to backup 'startup-config'. Check if flash has enough free space")
                self._logger.debug("Backup completed successfully")

                try:
                    restore_action.copy(path, "startup-config", action_map=copy_action_map)
                except:
                    self._logger.debug("Failed to reload 'startup-config' from {}.".format(path))
                    self._logger.debug("Restore 'startup-config' from backup")
                    restore_action.copy(self.BACKUP_STARTUP, "startup-config", action_map=copy_action_map)
                    raise

                restore_action.reload_device()

            elif configuration_type == "running-config" and restore_method == "append":
                try:
                    restore_action.copy(path, configuration_type, action_map=copy_action_map, timeout=5)
                except ExpectedSessionException:
                    pass
                if enable_session.session.session_type.lower() != "console":
                    enable_session.reconnect(timeout=self.SESSION_RECONNECT_TIMEOUT)
            else:
                restore_action.copy(path, configuration_type, action_map=copy_action_map)
