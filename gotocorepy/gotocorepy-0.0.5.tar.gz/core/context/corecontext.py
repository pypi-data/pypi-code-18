from core.base.corebaseparameterholder import CoreBaseParameterHolder
from core.service.coreservicecontainer import CoreServiceContainer


class CoreContext(CoreBaseParameterHolder):

    instance=None
    @staticmethod
    def getInstance():
        if (CoreContext.instance == None):
            CoreContext.instance = CoreContext()
        return CoreContext.instance;

    def __init__(self):
        self.sc = CoreServiceContainer.getInstance();

    def getParam(self,name):
        return self.params[name];

    def getString(self,name):
        return str(self.params[name]);

    def getInteger(self,name):
        return int(self.params[name]);

    def getNumber(self,name):
        return float(self.params[name]);

    def getParams(self):
        return self.params;


