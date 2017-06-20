import asyncio
import functools
import pickle
import logging

logger = logging.getLogger(__name__)

import ws_storage.packet
import ws_storage.protocol

class ClientProtocol(ws_storage.protocol.Protocol):

    def read_object(self, id_):
        p = ws_storage.packet.ReadObject(id_)
        return self.write(p)

    def write_object(self, id_, o):
        p = ws_storage.packet.WriteObject(id_, o)
        return self.write(p)

    def read_binary(self, id_):
        p = ws_storage.packet.ReadBinary(id_)
        return self.write(p)

    def write_binary(self, id_, b):
        p = ws_storage.packet.WriteBinary(id_, b)
        return self.write(p)


