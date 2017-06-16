from core.base.corebaseclass import CoreBaseClass
from core.utils.coreutils import CoreUtils


class CoreBaseLogger(CoreBaseClass):
    def __init__(self):
        self.br = "\n"

    def addLog(self, *messages):
        for message in messages:
            self.addLogEntry(str(message));

    def addLogEntry(self, message):
        print (message)

    def createEntryFrom(self, message):
        return (CoreUtils.timeStamp() + " ----> " + message);
