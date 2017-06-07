try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

class Resource(object):
    """
    Base class for all v3 REST Services
    """
    def __init__(self, attributes=None, api=None):
        self.__dict__['api'] = api
        self.__dict__['__data__'] = dict()
        self.merge_attributes(attributes)

    def merge_attributes(self, attributes):
        for (k, v) in attributes.items():
            setattr(self, k, v)
            self.__data__[k] = v

    def to_dict(self):
        return self.__data__

    def __setattr__(self, key, value):
        super(Resource, self).__setattr__(key, value)
        self.__data__[key] = value

    def __setitem__(self, key, value):
        if value and '__data__' in value:
            self.__data__[key] = value.__data__
        else:
            self.__data__[key] = value

    def __getitem__(self, item):
        return self.__data__.get(item, None)

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __contains__(self, item):
        return item in self.__data__


class Find(Resource):

    @classmethod
    def find(cls, resource_id, api=None):
        assert api is not None
        url = "{0}/{1}".format(cls.path, resource_id)
        return cls(attributes=api.get_request(url).json(), api=api)

    @classmethod
    def search(cls, params, api=None):
        assert api is not None
        assert params is not None
        assert type(params) is dict
        url = "{0}?{1}".format(cls.path, urlencode(params))
        all_result = api.get_request(url).json()
        if 'Items' in all_result:
            return [cls(attributes=object, api=api) for object in all_result['Items']]
        else:
            return []


class List(Resource):
    @classmethod
    def all(cls, api=None):
        all_result = api.get_request(cls.path).json()
        if 'Items' in all_result:
            return [cls(attributes=object, api=api) for object in all_result['Items']]
        else:
            return []


class Create(Resource):
    def create(self):
        response = self.api.post_request(self.path, self.to_dict())
        self.merge_attributes(response.json())


class Update(Resource):
    def update(self):
        update_payload = None
        try:
            update_payload = self.update_schema()
        except AttributeError:
            update_payload = self.to_dict()
        response = self.api.put_request("{0}/{1}".format(self.path, self['ID']), update_payload)
        try:
            self.merge_attributes(response.json())
        except ValueError:
            pass


class Delete(Resource):
    def delete(self):
        response = self.api.delete_request("{0}/{1}".format(self.path, self['ID']))
        self.merge_attributes(response.json())
