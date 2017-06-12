from __future__ import absolute_import

import json

from roundhouse import Serializer


class JSONSerializer(Serializer):
    """Handles serialization of JSON data"""

    format = 'json'
    extensions = ['.json']

    def serialize(self, data, stream):
        stream.write(json.dumps(data, indent=4 if self.pretty else None).encode())

        return stream

    def deserialize(self, stream):
        return json.loads(stream.read().decode('utf-8'))
