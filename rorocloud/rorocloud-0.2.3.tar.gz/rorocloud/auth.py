from __future__ import print_function
from os.path import expanduser, join, exists

try:
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

class AuthProvider:
    def get_auth(self):
        raise NotImplementedError()

    def set_auth(self, email, token):
        raise NotImplementedError()

class FileAuthProvider:
    def __init__(self, configfile=None):
        if configfile is None:
            configfile = join(expanduser("~"), ".rorocloudrc")
        self._configfile = configfile
        self.auth = self._read_auth()

    def get_auth(self):
        return self.auth

    def set_auth(self, email, token):
        self._write_auth(email, token)

    def _read_auth(self):
        if not exists(self._configfile):
            return

        p = configparser.ConfigParser()
        p.read(self._configfile)
        try:
            email = p.get("DEFAULT", "email")
            token = p.get("DEFAULT", "token")
            return (email, token)
        except configparser.NoOptionError:
            pass

    def _write_auth(self, email, token):
        p = configparser.ConfigParser()
        p.read(self._configfile)

        p.set("DEFAULT", "email", email)
        p.set("DEFAULT", "token", token)

        with open(self._configfile, "w") as f:
            p.write(f)

        print("Token saved in", self._configfile)
