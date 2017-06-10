import json
import threading

class Sender(object):
    def __init__(self):
        self.socket = None
        self.lock = threading.Lock()

    def send(self, reply):
        if not self.socket:
            return

        content = json.dumps(_clean_dict(reply))
        size = len(content)
        message = str(size) + ':' + content

        with self.lock:
            self.socket.sendall(message.encode())


def _clean_dict(data):
    if not isinstance(data, dict):
        return data

    new_dict = {}
    for key in data.keys():
        value = data[key]
        if value is not None:
            new_dict[key] = _clean_dict(value)

    return new_dict
