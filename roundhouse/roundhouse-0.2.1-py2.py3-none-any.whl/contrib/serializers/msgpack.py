from __future__ import absolute_import

import msgpack

from roundhouse import Serializer


class MsgPackSerializer(Serializer):

    format = 'msgpack'
    extensions = ['.mp', '.msgpack']

    def serialize(self, data, stream):
        msgpack.dump(data, stream, use_bin_type=True)

        return stream

    def deserialize(self, stream):
        return msgpack.load(stream, encoding='utf-8')
