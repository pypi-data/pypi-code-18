from core.base.corebaseclassfactory import CoreBaseClassFactory
from core.utils.log import Log


class CoreBaseClass(object):
    _nameIndex = 0
    _namePrefix = "core.base.class"

    def __init__(self):
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

    def log(self, *messages):
        m = ""
        for message in messages:
            m += str(message)
            m += " "
        Log.add(m)

    def generateName(self):
        CoreBaseClass._nameIndex += 1
        return CoreBaseClass._namePrefix + str(CoreBaseClass._nameIndex)