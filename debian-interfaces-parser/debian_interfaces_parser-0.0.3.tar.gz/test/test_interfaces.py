# -*- coding: utf-8 -*-

import unittest
import os

import debian_interfaces_parser.interfaces as interfaces
import debian_interfaces_parser.iface as iface


one_and_two_cases_dump = \
"""auto lo
iface lo inet loopback

auto eth0:0
iface eth0:0 inet static
  address 10.10.10.2
  netmask 255.255.255.252

auto eth0
iface eth0 inet static
  address 192.168.1.170
  netmask 255.255.255.0
  gateway 192.168.1.1
  dns-nameservers 192.168.1.1 8.8.8.8

auto wlan0
iface wlan0 inet dhcp
  wpa-ssid hello
  wpa-psk hello_123

"""


def load_fixture(name):
    return interfaces.Interfaces(os.path.dirname(os.path.realpath(__file__)) + '/' + name)


class InterfacesTest(unittest.TestCase):
    def test_case1(self):
        ifaces = load_fixture('interfaces1').parse_all()
        self.assertEqual(len(ifaces), 4)

        for i in ifaces:
            self.assertEqual(i.auto, True)
            if i.name == 'lo':
                self.assertEqual(i.src, 'loopback')
            elif i.name == 'eth0:0':
                self.assertEqual(i.src, 'static')
                self.assertEqual(i.address, '10.10.10.2')
                self.assertEqual(i.netmask, '255.255.255.252')
            elif i.name == 'eth0':
                self.assertEqual(i.src, 'static')
                self.assertEqual(i.address, '192.168.1.170')
                self.assertEqual(i.netmask, '255.255.255.0')
                self.assertEqual(i.gateway, '192.168.1.1')
                self.assertEqual(i.dns_nameservers, ['192.168.1.1', '8.8.8.8'])
            elif i.name == 'wlan0':
                self.assertEqual(i.src, 'dhcp')
                self.assertEqual(i.wpa_ssid, 'hello')
                self.assertEqual(i.wpa_psk, 'hello_123')

        self.assertEqual(interfaces.Interfaces.dump_all(ifaces), one_and_two_cases_dump)

    def test_case2(self):
        ifaces = load_fixture('interfaces2').parse_all()
        self.assertEqual(len(ifaces), 4)

        for i in ifaces:
            self.assertEqual(i.auto, True)
            if i.name == 'lo':
                self.assertEqual(i.src, 'loopback')
            elif i.name == 'eth0:0':
                self.assertEqual(i.src, 'static')
                self.assertEqual(i.address, '10.10.10.2')
                self.assertEqual(i.netmask, '255.255.255.252')
            elif i.name == 'eth0':
                self.assertEqual(i.src, 'static')
                self.assertEqual(i.address, '192.168.1.170')
                self.assertEqual(i.netmask, '255.255.255.0')
                self.assertEqual(i.gateway, '192.168.1.1')
                self.assertEqual(i.dns_nameservers, ['192.168.1.1', '8.8.8.8'])
            elif i.name == 'wlan0':
                self.assertEqual(i.src, 'dhcp')
                self.assertEqual(i.wpa_ssid, 'hello')
                self.assertEqual(i.wpa_psk, 'hello_123')

        self.assertEqual(interfaces.Interfaces.dump_all(ifaces), one_and_two_cases_dump)

    def test_case3(self):
        with self.assertRaises(iface.InvalidIface):
            load_fixture('interfaces3').parse_all()

