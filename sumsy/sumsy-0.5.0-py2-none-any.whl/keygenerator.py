import os

from Crypto.PublicKey import RSA


__metaclass__ = type


def _write_file(filename, content, mode):
    fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, 'w') as file:
        file.write(content)


class KeyGenerator:
    def __init__(self, config):
        self.key_name = config.key_name
        self.key_size = config.key_size

    def generate_key(self):
        key = RSA.generate(self.key_size)

        _write_file(self.key_name, key.exportKey(), 0o600)
        _write_file(self.key_name + '.pub', key.publickey().exportKey(), 0o644)

    run = generate_key
