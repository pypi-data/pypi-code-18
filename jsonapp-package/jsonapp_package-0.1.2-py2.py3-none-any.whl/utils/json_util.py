import collections
import json

import datetime


def dict_from(json_string):
    return JSONUtil(json_string).to_odict()


class JSONUtil(object):

    def __init__(self, json_input):

        self.json_input = json_input

    def to_odict(self, raise_exception=False):

        if raise_exception:

            if not self.valid_json:
                raise ValueError('Not a valid JSON string')

            return json.loads(self.json_input, object_pairs_hook=collections.OrderedDict)

        else:
            try:
                return json.loads(self.json_input, object_pairs_hook=collections.OrderedDict)
            except ValueError:
                return collections.OrderedDict()

    @property
    def valid_json(self):

        try:
            json.loads(self.json_input)
        except ValueError:
            return False

        return True

    def to_pretty_string(self):

        return json.dumps(self.json_input, indent=4)


JSON = JSONUtil


class JsonEnhanceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')

        return json.JSONEncoder.default(self, obj)
