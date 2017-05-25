import json


class DictUtil(object):

    def __init__(self, dict):
        self._dict = dict

    @property
    def dict(self):
        return self._dict

    def to_pretty_json_string(self):

        return json.dumps(self.dict, indent=4)

    def remove(self, key, allow_missing_key=False):

        if allow_missing_key:
            if key not in self.dict:
                return None

        del self.dict[key]


Dict = DictUtil
