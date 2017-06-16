from core.base.corebasefunctionwrapper import CoreBaseFunctionWrapper


class CoreService(CoreBaseFunctionWrapper):
    CORE_SERVICE_NAME = "core.service.name"

    def __init__(self, name, reference):
        super(CoreService, self).__init__(name, reference)

    def execute(self):
        return self.call()

    def clone(self):
        service = CoreService(self.name, self.reference)
        service.addParams(self.params)
        return service
