from core.base.corebaseparameterholder import CoreBaseParameterHolder


class CoreBaseFunctionWrapper(CoreBaseParameterHolder):
    def __init__(self, name, reference):
        super(CoreBaseFunctionWrapper, self).__init__()
        self.name = name
        self.reference = reference

    def call(self):
        return self.reference(self.params)

    def has(self, reference):
        return (self.reference == reference)

    def clone(self):
        return None
