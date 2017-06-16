from core.logger.base.corebaselogger import CoreBaseLogger


class CoreLoggerDebug(CoreBaseLogger):
    def addLogEntry(self, message):
        print self.createEntryFrom(message)
