from core.base.corebaseparameterholder import CoreBaseParameterHolder


class CoreBaseSender(CoreBaseParameterHolder):
    def __init__(self, name, collection):
        super(CoreBaseSender, self).__init__()
        self.name = name
        self.collection = collection
