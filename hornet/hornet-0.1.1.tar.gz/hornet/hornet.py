from collections import Mapping, MutableMapping


class Hornet(MutableMapping):
    @classmethod
    def object_pairs_hook(cls):
        return dict

    def __init__(self, items=(), **kwargs):
        self._underlying_mapping = self.object_pairs_hook()()
        if isinstance(items, Mapping):
            items = items.items()
        for k, v in items:
            if isinstance(v, Mapping):
                v = type(self)(v)
            self._underlying_mapping[k] = v
        for k, v in kwargs.items():
            if isinstance(v, Mapping):
                v = type(self)(v)
            self._underlying_mapping[k] = v

    def __getitem__(self, key):
        return self._underlying_mapping[key]

    def __setitem__(self, key, value):
        self._underlying_mapping[key] = value

    def __delitem__(self, key):
        del self._underlying_mapping[key]

    def __iter__(self):
        return iter(self._underlying_mapping)

    def __len__(self):
        return len(self._underlying_mapping)
