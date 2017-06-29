import json


class SingletonBuffer:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SingletonBuffer.__instance == None:
            SingletonBuffer()
        return SingletonBuffer.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SingletonBuffer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SingletonBuffer.__instance = self
            self.bufferString = ""
            self.bufferJsonArray = []

    # -----------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------

    def bufferString_clear(self, str):
        self.bufferString = ""

    def bufferString_add(self, str):
        self.bufferString += str.decode('utf8').encode('utf8') + "\n"

    def bufferString_get(self):
        return self.bufferString

    def bufferString_save(self, fileName, overWrite, clearVar):
        mod = "a"
        if overWrite: mod = "w"

        with open(fileName, mod) as f:
            f.write(self.bufferString)

        if clearVar: self.bufferString = ""
