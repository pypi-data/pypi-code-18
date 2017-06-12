from __future__ import absolute_import

import toml

from roundhouse import Serializer


class TOMLSerializer(Serializer):

    format = 'toml'
    extensions = ['.toml']

    def serialize(self, data, stream):
        stream.write(toml.dumps(data).encode())

        return stream

    def deserialize(self, stream):
        return toml.loads(stream.read().decode('utf-8'))
