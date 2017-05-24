import ujson as json

class DObject(object):
    def __init__(self, dictionary={}):
        self.__dict__.update(dictionary)
        for k, v in dictionary.items():
            if isinstance(v, dict):
                self.__dict__[k] = DObject(v)
            elif isinstance(v, list):
                if len(v) > 0  and isinstance(v[0], dict):
                    self.__dict__[k] = [DObject(_v) for _v in v]

    def __eq__(self, other):
        if hasattr(other, 'to_dict'):
            other = other.to_dict()
        elif hasattr(other, '__dict__'):
            other = other.__dict__
        return self.to_dict() == other

    def __getitem__(self, key):
        return self.to_dict()[key]

    def to_dict(self):
        return self.__dict__

    def to_json(self, filename=None):
        d = self.to_dict()
        if filename:
            json.dump(open(filename, 'w'), d)
        return json.dumps(d)

    @classmethod
    def from_json(cls, filename=None, string=None):
        if filename:
            data = json.load(open(filename))
        elif string:
            data = json.loads(string)
        else:
            raise Exception("No file or string provided")
        return cls(data)
