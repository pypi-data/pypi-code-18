from __future__ import absolute_import

import pickle

from roundhouse import Serializer


class PickleSerializer(Serializer):

    format = 'pickle'
    extensions = ['.pkl']

    def serialize(self, data, stream):
        pickle.dump(data, stream)

        return stream

    def deserialize(self, stream):
        return pickle.load(stream)
