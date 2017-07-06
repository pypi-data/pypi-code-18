#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.firewall.cisco.asa.command_templates import configuration, firmware


class SystemActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    @staticmethod
    def prepare_action_map(source_file, destination_file):
        action_map = OrderedDict()
        host = None
        if "://" in destination_file:
            destination_file_data_list = re.sub("/+", "/", destination_file).split("/")
            host = destination_file_data_list[1]
            source_file_name = source_file.split(":")[-1].split("/")[-1]
            action_map[r"[\[\(].*{}[\)\]]".format(destination_file_data_list[-1])] = lambda session, logger: session.send_line("", logger)

            action_map[r"[\[\(]{}[\)\]]".format(source_file_name)] = lambda session, logger: session.send_line("", logger)
        else:
            destination_file_name = destination_file.split(":")[-1].split("/")[-1]
            source_file_name = source_file.split(":")[-1].split("/")[-1]
            action_map[r"(?!/)[\[\(]{}[\)\]]".format(
                destination_file_name)] = lambda session, logger: session.send_line("", logger)
            action_map[r"(?!/)[\[\(]{}[\)\]]".format(
                source_file_name)] = lambda session, logger: session.send_line("", logger)
        if host:
            if "@" in host:
                storage_data = re.search(r"^(?P<user>\S+):(?P<password>\S+)@(?P<host>\S+)", host)
                if storage_data:
                    storage_data_dict = storage_data.groupdict()
                    host = storage_data_dict["host"]
                    username = storage_data_dict["user"]
                    password = storage_data_dict["password"]

                    action_map[r"[\[\(]{}[\)\]]".format(username)] = lambda session, logger: session.send_line("", logger)
                    action_map[r"[\[\(]{}[\)\]]".format(password)] = lambda session, logger: session.send_line("", logger)
                    action_map[r"[Pp]assword:".format(source_file)] = lambda session, logger: session.send_line(password, logger)
                else:
                    host = host.split("@")[-1]
            action_map[r"(?!/){}(?!/)".format(host)] = lambda session, logger: session.send_line("", logger)

        action_map[r"\?"] = lambda session: session.send_line("")
        return action_map

    def copy(self, source, destination, action_map=None, error_map=None, timeout=None, noconfirm=True):
        """ Copy file from device to tftp or vice versa, as well as copying inside devices filesystem.

        :param source: source file
        :param destination: destination file
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :param timeout: session timeout
        :raise Exception:
        """

        if noconfirm:
            output = CommandTemplateExecutor(self._cli_service, configuration.COPY,
                                             action_map=action_map,
                                             error_map=error_map,
                                             timeout=timeout).execute_command(src=source,
                                                                              dst=destination,
                                                                              noconfirm="")

            if "Invalid input detected" in output:
                output = CommandTemplateExecutor(self._cli_service, configuration.COPY,
                                                 action_map=action_map,
                                                 error_map=error_map).execute_command(src=source,
                                                                                      dst=destination)

        else:
            output = CommandTemplateExecutor(self._cli_service, configuration.COPY,
                                             action_map=action_map,
                                             error_map=error_map).execute_command(src=source,
                                                                                  dst=destination)

        copy_ok_pattern = r"\d+ bytes copied|copied.*[\[\(].*[1-9][0-9]* bytes.*[\)\]]|[Cc]opy complete|[\(\[]OK[\]\)]"
        status_match = re.search(copy_ok_pattern, output, re.IGNORECASE)

        if not status_match:
            match_error = re.search(r"%.*|TFTP put operation failed.*|sysmgr.*not supported.*\n",
                                    output,
                                    re.IGNORECASE)
            message = "Copy Command failed. "
            if match_error:
                self._logger.error(message)
                message += re.sub(r"^%|\\n", "", match_error.group())
            else:
                error_match = re.search(r"error.*\n|fail.*\n", output, re.IGNORECASE)
                if error_match:
                    self._logger.error(message)
                    message += error_match.group()
            raise Exception("Copy", message)

    def reload_device(self, timeout=500, action_map=None, error_map=None):
        """Reload device

        :param timeout: session reconnect timeout
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        try:
            CommandTemplateExecutor(self._cli_service, configuration.RELOAD).execute_command(
                action_map=action_map, error_map=error_map)
        except Exception as e:
            self._logger.info("Device rebooted, starting reconnect")
        self._cli_service.reconnect(timeout)

    def reload_device_via_console(self, timeout=500, action_map=None, error_map=None):
        """Reload device

        :param session: current session
        :param logger:  logger
        :param timeout: session reconnect timeout
        """

        CommandTemplateExecutor(self._cli_service, configuration.CONSOLE_RELOAD, action_map=action_map,
                                error_map=error_map).execute_command(timeout=timeout)

    def get_current_boot_config(self, action_map=None, error_map=None):
        """Retrieve current boot configuration

        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return:
        """

        return CommandTemplateExecutor(self._cli_service, firmware.SHOW_RUNNING, action_map=action_map,
                                       error_map=error_map).execute_command()

    def get_current_os_version(self, action_map=None, error_map=None):
        """Retrieve os version

        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return:
        """

        return CommandTemplateExecutor(self._cli_service, firmware.SHOW_VERSION, action_map=action_map,
                                       error_map=error_map).execute_command()

    def shutdown(self):
        """
        Shutdown the system
        :return:
        """
        pass


class FirmwareActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def install_firmware(self, firmware_file_name):
        """Set boot firmware file.

        :param firmware_file_name: firmware file name
        """

        CommandTemplateExecutor(self._cli_service, firmware.BOOT_SYSTEM_FILE).execute_command(
            firmware_file_name=firmware_file_name)
        CommandTemplateExecutor(self._cli_service, firmware.CONFIG_REG).execute_command()
