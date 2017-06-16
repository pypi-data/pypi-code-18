from core.service.coreservicecontainer import CoreServiceContainer


class Log(object):

    def __init__(self):
        super(Log, self).__init__()

    @staticmethod
    def add(message):
        if not CoreServiceContainer.getInstance().hasService('logger.log'):
            return;
        CoreServiceContainer.getInstance()\
            .getService('logger.log')\
            .addParam('message', message)\
            .execute();

    @staticmethod
    def error(message):
        Log.add("<font color='#FF0000'>" + message + "</font>")

    @staticmethod
    def major(message):
        Log.add("<font color='#000FFFF'>" + message + "</font>")
