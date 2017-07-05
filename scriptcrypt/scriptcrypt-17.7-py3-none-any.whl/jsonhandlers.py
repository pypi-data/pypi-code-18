import json
import os.path
from os import environ, makedirs


class JSONHandler(object):

    def __init__(self, path, default):
        self.fpath = path
        self.default = default

    def writeData(self, settings):
        with open(self.fpath, "w") as f:
            f.write(json.dumps(settings,
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': ')))

    def readData(self):
        with open(self.fpath, "r") as f:
            dump = f.read()

        return json.loads(dump)

    def writeDefault(self):
        self.writeData(self.default)

    def getData(self):
        if not os.path.isfile(self.fpath):
            try:
                makedirs(os.path.dirname(self.fpath))
            except FileExistsError:
                pass
            self.writeDefault()
        return self.readData()


class Settigns(JSONHandler):
    def __init__(self):
        home = environ["HOME"]
        super().__init__(home + "/.config/scriptcrypt" + "/settings.json",
                         {"editor": "nano",
                          "viewer": "less",
                          "shell": "sh",
                          "transparent_bkgr": True,
                          "db": home + "/.scriptcrypt.db"})


class Envars(JSONHandler):
    def __init__(self):
        home = environ["HOME"]
        super().__init__(home + "/.config/scriptcrypt" + "/envars.json",
                         {"INSTALL": "sudo apt-get install -y",
                          "UNINSTALL": "sudo apt-get remove -y",
                          "UPDATE": "sudo apt-get update",
                          "APPDIR": home + "/Applications"})
