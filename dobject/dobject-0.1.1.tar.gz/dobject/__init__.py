import json


class DObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DObject):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

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

    def to_json(self, filename=None, cls=DObjectEncoder):
        d = self.to_dict()
        if filename:
            json.dump(open(filename, 'w'), d, cls=cls)
        return json.dumps(d, cls=cls)

    @classmethod
    def from_json(klass, filename=None, string=None, cls=json.JSONDecoder):
        if filename:
            data = json.load(open(filename), cls=cls)
        elif string:
            data = json.loads(string, cls=cls)
        else:
            raise Exception("No file or string provided")
        return klass(data)
