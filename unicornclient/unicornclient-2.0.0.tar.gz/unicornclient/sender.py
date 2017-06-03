import json
from . import spy

class Sender(object):
    def __init__(self):
        self.socket = None

    def send(self, reply):
        if not self.socket:
            return
        content = json.dumps(_clean_dict(reply))
        size = len(content)
        message = str(size) + ':' + content
        self.socket.sendall(message.encode())

    def authenticate(self):
        payload = {
            'type':'auth',
            'serial': spy.get_serial()
        }
        self.send(payload)

    def send_status(self):
        payload = {
            'type':'status',
            'status': self.get_status()
        }
        self.send(payload)

    def get_status(self):
        status = {
            'hostname': spy.get_hostname(),
            'local_ip': spy.get_local_ip(),
            'addresses': spy.get_macs(),
            'ssid': spy.get_ssid(),
            'temp': spy.get_temp(),
            'signal_level': spy.get_signal_level(),
            'written_kbytes': spy.get_written_kbytes(),
            'uptime': spy.get_uptime()
        }
        return status


def _clean_dict(data):
    if not isinstance(data, dict):
        return data

    new_dict = {}
    for key in data.keys():
        value = data[key]
        if value is not None:
            new_dict[key] = _clean_dict(value)

    return new_dict
