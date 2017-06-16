from core.base.corebasesender import CoreBaseSender
from core.service.coreservicecontainer import CoreServiceContainer


class CoreCallback(CoreBaseSender):
    GROUP = 'group'
    CALLBACK = 'callback'
    CALLBACKS = 'callbacks'

    ADD_CALLBACK = ".add.callback"
    ADD_CALLBACKS = ".add.callbacks"

    REMOVE_CALLBACKS = ".remove.callbacks"
    REMOVE_CALLBACK = ".remove.callback"

    def __init__(self, name, collection):
        super(CoreCallback, self).__init__(name, collection)

    def send(self):
        for service in self.collection:
            print "send callback:", service
            service.addParams(self.params).execute()

    @staticmethod
    def addCallback(target, group, callback):
        CoreServiceContainer.getInstance().getService(target.name + CoreCallback.ADD_CALLBACK)\
            .addParam(CoreCallback.GROUP, group)\
            .addParam(CoreCallback.CALLBACK, callback)\
            .execute()

    @staticmethod
    def addCallbacks(target, group, callbacks):
        CoreServiceContainer.getInstance().getService(target.name + CoreCallback.ADD_CALLBACKS)\
            .addParam(CoreCallback.GROUP, group)\
            .addParam(CoreCallback.CALLBACKS, callbacks)\
            .execute()

    @staticmethod
    def removeCallbacks(target, group, callbacks):
        CoreServiceContainer.getInstance().getService(target.name + CoreCallback.REMOVE_CALLBACKS)\
            .addParam(CoreCallback.GROUP, group)\
            .addParam(CoreCallback.CALLBACKS, callbacks)\
            .execute()
