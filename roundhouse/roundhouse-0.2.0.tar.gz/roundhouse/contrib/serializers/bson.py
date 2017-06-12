from __future__ import absolute_import

import bson

from roundhouse import Serializer


class BSONSerializer(Serializer):

    format = 'bson'
    extensions = ['.bson']

    def serialize(self, data, stream):
        stream.write(bson.dumps(data))

        return stream

    def deserialize(self, stream):
        return bson.loads(stream.read())
