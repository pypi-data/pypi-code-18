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

    def bufferString_set(self, str):
        self.bufferString = str.decode(encoding="utf-8", errors="replace") + "\n"

    def bufferString_add(self, str):
        self.bufferString += str.decode(encoding="utf-8", errors="replace") + "\n"

    def bufferString_get(self):
        return self.bufferString

    def bufferString_save(self, fileName, overWrite):
        mod = "a"
        if overWrite: mod = "w"

        with open(fileName, mod) as f:
            f.write(self.bufferString)

    # -----------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------

    def bufferJsonArray_set(self, jobjArr):
        self.bufferJsonArray = jobjArr

    def bufferJsonArray_append(self, jobj):
        self.bufferJsonArray.append(jobj)

    def bufferJsonArray_get(self):
        return self.bufferJsonArray

    def bufferJsonArray_save(self, fileName, overWrite):
        mod = "a"
        if overWrite: mod = "w"
        with open(fileName, mod) as f:
            f.write(json.dumps(self.bufferString))


            # SingletonBuffer.getInstance().bufferString_add(str=u"\xe8"+"kkkk")
            # print SingletonBuffer.getInstance().bufferString_get()
