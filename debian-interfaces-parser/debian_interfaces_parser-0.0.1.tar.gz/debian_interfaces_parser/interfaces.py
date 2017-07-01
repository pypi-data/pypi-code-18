# -*- coding: utf-8 -*-

import re

import debian_interfaces_parser.iface as iface


class Interfaces(object):
    def __init__(self, path='/etc/network/interfaces'):
        self.path = path
        self.data = self.read().strip()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read().strip()

    def parse_all(self):
        ifaces = []
        autos = []
        for line in self.data.split('\n'):
            iface_match = re.search('^iface (.+) inet (static|dhcp|loopback)$', line)
            if iface_match:
                name = iface_match.group(1)
                src = iface_match.group(2)
                ifaces.append(iface.Iface(name, src))
                continue

            cfg_match = re.search('^\s+(address|netmask|gateway|dns-nameservers|wpa-ssid|wpa-psk) (.+)$', line)
            if cfg_match:
                key = cfg_match.group(1)
                value = cfg_match.group(2).strip()
                ifc = ifaces[-1]
                if key == 'address':
                    ifc.address = value
                elif key == 'netmask':
                    ifc.netmask = value
                elif key == 'dns-nameservers':
                    ifc.dns_nameservers = [i.strip() for i in value.split(',')]
                elif key == 'gateway':
                    ifc.gateway = value
                elif key == 'wpa-ssid':
                    ifc.wpa_ssid = value
                elif key == 'wpa-psk':
                    ifc.wpa_psk = value

            auto_match = re.search('^auto (.+)$', line)
            if auto_match:
                ifc_name = auto_match.group(1).strip()
                autos.append(ifc_name)

        for i in ifaces:
            if i.name in autos:
                i.auto = True
            i.validate()

        return ifaces

    def write(self, data):
        with open(self.path, 'w') as f:
            return f.write(data)

    @staticmethod
    def dump_all(interfaces):
        result = ''
        for i in interfaces:
            result += i.dump()
            result += '\n'

        return result






