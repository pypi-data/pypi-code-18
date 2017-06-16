from core.base.corebasefunctionwrapper import CoreBaseFunctionWrapper
from core.service.coreservicecontainer import CoreServiceContainer


class CoreListener(CoreBaseFunctionWrapper):

    REGISTER_LISTENER = "core.listener.register.listener"
    REGISTER_LISTENERS = "core.listener.register.listeners"
    REMOVE_LISTENERS_BY_NAME = "core.listener.remove.listeners.by.name"
    REMOVE_LISTENER = "core.listener.remove.listener"
    REMOVE_LISTENERS = "core.listener.remove.listeners"
    REFERENCE = "reference"
    LISTENER = "listener"
    NAME = "name"
    BASE_NAME = "base.name"

    def __init__(self, name, reference):
        super(CoreListener, self).__init__(name, reference)

    def notify(self):
        self.call()

    @staticmethod
    def register(name, callback):
        listener = CoreListener(name, callback)
        sc = CoreServiceContainer.getInstance()
        sc.getService(CoreListener.REGISTER_LISTENER)\
            .addParam(CoreListener.LISTENER, listener)\
            .addParam(CoreListener.NAME, name).execute()

    @staticmethod
    def registerForClass(c, callback):
        name = c.__name__
        listener = CoreListener(name, callback)
        CoreServiceContainer.getInstance()\
            .getService(CoreListener.REGISTER_LISTENER)\
            .addParam(CoreListener.LISTENER, listener)\
            .addParam(CoreListener.NAME, name).execute()

    @staticmethod
    def registers(names, callback):
        for name in names:
            CoreListener.register(name, callback)

    @staticmethod
    def unregister(name, callback):
        CoreServiceContainer.getInstance().getService(CoreListener.REMOVE_LISTENER).addParam(CoreListener.NAME, name).addParam(CoreListener.REFERENCE, callback).execute()

    @staticmethod
    def unregisterFromClass(c, callback):
        name = c.__name__
        CoreServiceContainer.getInstance().getService(CoreListener.REMOVE_LISTENER).addParam(CoreListener.NAME, name).addParam(CoreListener.REFERENCE, callback).execute()