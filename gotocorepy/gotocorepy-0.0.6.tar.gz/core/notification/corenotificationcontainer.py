from core.base.corebaseclass import CoreBaseClass
from core.notification.corelistener import CoreListener
from core.notification.corenotification import CoreNotification


class CoreNotificationContainer(CoreBaseClass):
    instance = None

    @staticmethod
    def getInstance():
        if (CoreNotificationContainer.instance == None):
            CoreNotificationContainer.instance = CoreNotificationContainer()
        return CoreNotificationContainer.instance

    def __init__(self):
        super(CoreNotificationContainer, self).__init__()

        self.sc.registerService(CoreListener.REGISTER_LISTENER, self.registerListener)
        self.sc.registerService(CoreListener.REMOVE_LISTENER, self.removeListener)
        self.sc.registerService(CoreNotification.CREATE_NOTIFICATION, self.createNotification)
        self.mapping = {}

    def registerListener(self, params):
        name = params.get('name')
        listener = params.get('listener')

        if not self.hasListener(name):
            self.mapping[name] = []

        self.getListenersOf(name).append(listener);

    def removeListener(self, params):
        name = params.name
        reference = params.reference

        listeners= self.getListenersOf(name)
        index = self.getListenerBy(reference, listeners);

        if index != -1:
            del listeners[index];

    def getListenerBy(self,reference, listeners):
        for listener in listeners:
            if listener.has(reference):
                return listeners.indexOf(listener);
        return -1;

    def createNotification(self, params):
        name = params.get('name')
        return CoreNotification(name, self.getListenersOf(name));

    def hasListener(self, name):
        return self.mapping.has_key(name)

    def getListenersOf(self, name):
        if self.hasListener(name):
            return self.mapping.get(name)
        return []

