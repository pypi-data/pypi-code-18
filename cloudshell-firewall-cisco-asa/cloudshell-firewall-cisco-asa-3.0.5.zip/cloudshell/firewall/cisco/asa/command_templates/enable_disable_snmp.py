#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate

SHOW_IP_ADDR  =CommandTemplate("show ip address | inc {ip_address}")
SHOW_SNMP_COMMUNITY = CommandTemplate("more system:running-config | inc snmp-server host .* community")
ENABLE_SNMP_SERVER = CommandTemplate("snmp-server enable")
ENABLE_SNMP = CommandTemplate("snmp-server host {iface_name} {hostname} poll community {snmp_community} version 2c")
DISABLE_SNMP = CommandTemplate("no snmp-server host {iface_name} {hostname} poll community {snmp_community} version 2c")
