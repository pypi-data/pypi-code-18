from collections import OrderedDict

from RGPageRank.BaseTransformer import BaseTransformer


class DictTransformer(BaseTransformer):

    def prepare(self, data):
        if isinstance(data, dict):
            return OrderedDict(data)
        elif isinstance(data, OrderedDict):
            return data
        else:
            raise TypeError('Only dict and OrderedDict accepted for the class')
