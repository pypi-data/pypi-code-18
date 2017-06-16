from core.base.corebaseclass import CoreBaseClass


class CoreLogger(CoreBaseClass):
    LOGGER_LOG = "logger.log"
    MESSAGE = "message"
    instance=None

    def __init__(self,loggers):
        super(CoreLogger, self).__init__()
        self.loggers = loggers
        self.sc.registerService(CoreLogger.LOGGER_LOG, self.serviceLog)

    @staticmethod
    def getInstance(loggers):
        if (CoreLogger.instance == None):
            CoreLogger.instance = CoreLogger(loggers)
        return CoreLogger.instance

    def serviceLog(self,params):
        for logger in self.loggers:
            logger.addLog(params[CoreLogger.MESSAGE])
