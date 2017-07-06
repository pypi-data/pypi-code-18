#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow import CiscoASARestoreFlow
from cloudshell.cli.session.session_exceptions import ExpectedSessionException


class TestCiscoASARestoreFlow(unittest.TestCase):
    def setUp(self):
        super(TestCiscoASARestoreFlow, self).setUp()
        self.cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        self.tested_instance = CiscoASARestoreFlow(cli_handler=self.cli_handler, logger=logger)

    def tearDown(self):
        super(TestCiscoASARestoreFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_startup_override(self, system_actions_class):
        """ Restore startup-config in override mode. Success """

        path = mock.MagicMock()
        configuration_type = "startup"
        restore_method = "override"

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()

        self.tested_instance.execute_flow(path, configuration_type, restore_method)

        sys_actions.copy.assert_called_once_with(path,
                                                 "{}-config".format(configuration_type),
                                                 action_map=action_map)

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_startup_append(self, system_actions_class):
        """ Restore startup-config in append mode. Success """

        path = mock.MagicMock()
        configuration_type = "startup"
        restore_method = "append"

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()

        self.tested_instance.execute_flow(path, configuration_type, restore_method)

        sys_actions.copy.assert_called_once_with(path,
                                                 "{}-config".format(configuration_type),
                                                 action_map=action_map)

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_running_override_success(self, system_actions_class):
        """ Restore running-config in override mode. Success """

        path = mock.MagicMock()
        configuration_type = "running"
        restore_method = "override"

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()

        self.tested_instance.execute_flow(path, configuration_type, restore_method)

        self.assertEqual(sys_actions.copy.call_count, 2)

        sys_actions.copy.assert_any_call("startup-config", self.tested_instance.BACKUP_STARTUP, action_map=action_map)
        sys_actions.copy.assert_any_call(path, "startup-config".format(configuration_type), action_map=action_map)
        sys_actions.reload_device.assert_called_once()

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_running_override_fail_backup_startup(self, system_actions_class):
        """ Restore running-config in override mode. Backup startup-config failed """

        path = mock.MagicMock()
        configuration_type = "running"
        restore_method = "override"

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()
        sys_actions.copy = mock.MagicMock(side_effect=[Exception("Failed to backup 'startup-config'")])

        with self.assertRaisesRegexp(Exception, "Failed to backup 'startup-config'"):
            self.tested_instance.execute_flow(path, configuration_type, restore_method)

        sys_actions.copy.assert_called_once_with("startup-config",
                                                 self.tested_instance.BACKUP_STARTUP,
                                                 action_map=action_map)
        sys_actions.reload_device.assert_not_called()

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_running_override_fail_reload_startup(self, system_actions_class):
        """ Restore running-config in override mode. Reload startup-config failed """

        path = mock.MagicMock()
        configuration_type = "running"
        restore_method = "override"

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()
        sys_actions.copy = mock.MagicMock(side_effect=[None, Exception("Failed to reload 'startup-config'"), None])

        with self.assertRaisesRegexp(Exception, "Failed to reload 'startup-config'"):
            self.tested_instance.execute_flow(path, configuration_type, restore_method)

        self.assertEqual(sys_actions.copy.call_count, 3)

        sys_actions.copy.assert_any_call("startup-config",
                                         self.tested_instance.BACKUP_STARTUP,
                                         action_map=action_map)

        sys_actions.copy.assert_any_call(path, "startup-config", action_map=action_map)
        sys_actions.copy.assert_any_call(self.tested_instance.BACKUP_STARTUP, "startup-config", action_map=action_map)
        sys_actions.reload_device.assert_not_called()

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_running_append_console_success(self, system_actions_class):
        """ Restore running-config in append mode using CONSOLE session """

        path = mock.MagicMock()
        configuration_type = "running"
        restore_method = "append"
        session = mock.MagicMock(session_type="console")
        self.cli_handler.get_cli_service.return_value = mock.MagicMock(
            __enter__=mock.MagicMock(
                return_value=mock.MagicMock(session=session)
            ))

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()
        sys_actions.copy = mock.MagicMock(side_effect=[ExpectedSessionException])

        self.tested_instance.execute_flow(path, configuration_type, restore_method)

        sys_actions.copy.assert_called_once_with(path,
                                                 "{}-config".format(configuration_type),
                                                 action_map=action_map,
                                                 timeout=5)

        session.reconnect.assert_not_called()

    @mock.patch("cloudshell.firewall.cisco.asa.flows.cisco_asa_restore_flow.SystemActions")
    def test_execute_flow_running_append_console_success(self, system_actions_class):
        """ Restore running-config in append mode using NOT CONSOLE session """

        path = mock.MagicMock()
        configuration_type = "running"
        restore_method = "append"
        session = mock.MagicMock(session=mock.MagicMock(session_type="not_console"))
        self.cli_handler.get_cli_service.return_value = mock.MagicMock(__enter__=mock.MagicMock(return_value=session))

        sys_actions = mock.MagicMock()
        system_actions_class.return_value = sys_actions
        action_map = sys_actions.prepare_action_map()
        sys_actions.copy = mock.MagicMock(side_effect=[ExpectedSessionException])

        self.tested_instance.execute_flow(path, configuration_type, restore_method)

        sys_actions.copy.assert_called_once_with(path,
                                                 "{}-config".format(configuration_type),
                                                 action_map=action_map,
                                                 timeout=5)

        session.reconnect.assert_called_once_with(timeout=self.tested_instance.SESSION_RECONNECT_TIMEOUT)
