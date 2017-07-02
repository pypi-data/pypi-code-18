class ZooAbstract(object):
    def __init__(self):
        self.foobar = []
        self.animals = {'lions': 3}

    def __iter__(self):
        return iter(vars(self).items())


class Zoo(ZooAbstract):
    def add_lion(self):
        self.animals['lions'] += 1
