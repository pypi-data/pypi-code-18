import yaml


class Config(object):
    def __init__(self, file):
        with open(file) as f:
            self.cf = yaml.load(f)

    def get(self, key):
        return self.cf.get(key)
