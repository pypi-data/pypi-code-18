class CoreBaseParameterHolder(object):
    def __init__(self):
        self.params = {}

    def addParam(self, name, value):
        self.params[name] = value
        return self

    def addParams(self, params):
        for key in params:
            self.addParam(key, params[key])
        return self

    def notify(self):
        pass

    def execute(self):
        return None;

    def send(self):
        pass
