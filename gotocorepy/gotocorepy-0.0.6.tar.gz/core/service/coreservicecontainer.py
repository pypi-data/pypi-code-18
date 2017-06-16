from core.service.coreservice import CoreService


class CoreServiceContainer:
    instance = None

    @staticmethod
    def getInstance():
        if (CoreServiceContainer.instance == None):
            CoreServiceContainer.instance = CoreServiceContainer();
        return CoreServiceContainer.instance;

    def __init__(self):
        self.mapping = {}

    def registerService(self, name, reference):
        self.mapping[name] = reference;

    def updateService(self, name, reference):
        if (self.mapping[name]):
            self.mapping[name] = reference;

    def removeService(self, name):
        del self.mapping[name];

    def getService(self, name):
        if not self.mapping.has_key(name):
            # Log..error("Nincs ilyen service regisztrálva:  " + name);
            # ExternalInterface.call(  'alert'  ,  "Nincs ilyen service regisztrálva:  "  +  name  );
            # throw new Error("Nincs ilyen service regisztrálva:  " + name);
            raise ValueError("Nincs ilyen service regisztrálva:  " + name)



        return CoreService(name, self.mapping[name]).addParam(CoreService.CORE_SERVICE_NAME, name)

    def hasService(self,name):
        return (self.mapping[name] != None);
