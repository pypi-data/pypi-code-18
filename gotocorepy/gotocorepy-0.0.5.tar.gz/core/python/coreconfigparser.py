from ConfigParser import ConfigParser

from core.base.corebaseclassfactory import CoreBaseClassFactory
from core.utils.log import Log


class CoreConfigParser(ConfigParser):
    _nameIndex = 0
    _namePrefix = "core.config.parser"

    def __init__(self):
        super(CoreConfigParser, self).__init__()
        self.sc = None
        self.context = None
        self.callbacks = {}
        self.name = self.generateName()
        CoreBaseClassFactory.construct(self)


    def get_name(self):
        return self.name

    def serviceAddCallback(self, params):
        CoreBaseClassFactory.serviceAddCallback(self, params);

    def serviceAddCallbacks(self, params):
        CoreBaseClassFactory.serviceAddCallbacks(self, params)

    def serviceRemoveCallback(self, params):
        CoreBaseClassFactory.serviceRemoveCallback(self, params);

    def serviceRemoveCallbacks(self, params):
        CoreBaseClassFactory.serviceRemoveCallbacks(self, params);

    def createCallBack(self, group):
        return CoreBaseClassFactory.createCallBack(self, group);

    def log(self, message):
        Log.add(message)

    def generateName(self):
        CoreConfigParser._nameIndex += 1
        return CoreConfigParser._namePrefix + str(CoreConfigParser._nameIndex)