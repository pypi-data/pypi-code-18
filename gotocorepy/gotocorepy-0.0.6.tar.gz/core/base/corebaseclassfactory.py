import array

from core.base.corecallback import CoreCallback
from core.context.corecontext import CoreContext
from core.service.coreservicecontainer import CoreServiceContainer


class CoreBaseClassFactory:
    def __init__(self):
        pass

    @staticmethod
    def construct( _instance):
        _instance.sc = CoreServiceContainer.getInstance()
        _instance.context = CoreContext.getInstance()
        _instance.sc.registerService(_instance.name + CoreCallback.ADD_CALLBACK, _instance.serviceAddCallback)
        _instance.sc.registerService(_instance.name + CoreCallback.ADD_CALLBACKS, _instance.serviceAddCallbacks)
        _instance.sc.registerService(_instance.name + CoreCallback.REMOVE_CALLBACK, _instance.serviceRemoveCallback)
        _instance.sc.registerService(_instance.name + CoreCallback.REMOVE_CALLBACKS, _instance.serviceRemoveCallbacks)

    @staticmethod
    def serviceAddCallback(_instance, params):
        group = params[CoreCallback.GROUP]
        callback = params[CoreCallback.CALLBACK]
        CoreBaseClassFactory.addCallback(_instance, group, callback)

    @staticmethod
    def serviceRemoveCallback(_instance, params):
        group = params[CoreCallback.GROUP]
        callback = params[CoreCallback.CALLBACK]
        CoreBaseClassFactory.removeCallback(_instance, group, callback)

    @staticmethod
    def serviceAddCallbacks( _instance, params):
        group = params[CoreCallback.GROUP]
        callbacks = params[CoreCallback.CALLBACKS]

        for callback in callbacks:
            CoreBaseClassFactory.addCallback(_instance, group, callback)

    @staticmethod
    def serviceRemoveCallbacks( _instance, params):
        group = params[CoreCallback.GROUP]
        _instance.callbacks[group] = None

    @staticmethod
    def createCallBack(_instance, group):
        return CoreCallback(group, _instance.callbacks.get(group, []))

    @staticmethod
    def addCallback(_instance, group, callback):
        if not _instance.callbacks.has_key(group):
            _instance.callbacks[group] = []

        _instance.callbacks[group].append(callback)
        print _instance.callbacks

    @staticmethod
    def removeCallback(_instance, group, callback):
        if (_instance.callbacks[group] == None):
            return

        index = array(_instance.callbacks).indexOf(callback)
        array(_instance.callbacks).splice(index, 1)

    @staticmethod
    def log(_instance, message):
        if (_instance.sc.hasService("logger.log")):
            _instance.sc.getService("logger.log").addParam("message", message).execute()
