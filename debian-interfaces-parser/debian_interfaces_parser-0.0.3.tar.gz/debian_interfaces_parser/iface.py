# -*- coding: utf-8 -*-


class InvalidIface(RuntimeError):
    pass


class Iface(object):
    def __init__(self, name, src):
        self.src = src  # static or dhcp or loopback
        self.name = name
        self.netmask = None
        self.gateway = None
        self.dns_nameservers = []
        self.address = None
        self.wpa_ssid = None
        self.wpa_psk = None
        self.auto = False

    def dump(self):
        result = ''
        if self.auto:
            result += "auto {name}\n".format(name=self.name.strip())
        result += "iface {name} inet {src}\n".format(name=self.name, src=self.src.strip())

        if self.wpa_ssid and self.wpa_psk:
            result += "  wpa-ssid {s}\n".format(s=self.wpa_ssid.strip())
            result += "  wpa-psk {s}\n".format(s=self.wpa_psk.strip())

        if self.src == 'dhcp' or self.src == 'loopback':
            return result

        self.validate()

        result += "  address {s}\n".format(s=self.address.strip())
        result += "  netmask {s}\n".format(s=self.netmask.strip())

        if self.gateway:
            result += "  gateway {s}\n".format(s=self.gateway.strip())

        if len(self.dns_nameservers) > 0:
            result += "  dns-nameservers {s}\n".format(s=' '.join([i.strip() for i in self.dns_nameservers]))

        return result

    def validate(self):
        if self.src == 'static':
            if not self.address:
                raise InvalidIface('static interface must have address')
            if not self.netmask:
                raise InvalidIface('static interface must have netmask')




