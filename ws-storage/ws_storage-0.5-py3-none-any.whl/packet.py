
import asyncio
import logging

logger = logging.getLogger(__name__)

class Packet(object):
    async def __call__(self, proto):
        pass

class WriteObject(Packet):
    def __init__(self, id_, o):
        self.id_ = id_
        self.o = o

    async def __call__(self, proto):
        logger.debug('{} call'.format(self.__class__.__name__))

        proto.app.write_object(self.id_, self.o)

class ReadObject(Packet):
    def __init__(self, id_):
        self.id_ = id_

    async def __call__(self, proto):
        logger.debug('{} call'.format(self.__class__.__name__))

        o = await proto.app.read_object(self.id_)

        logger.debug('o={}'.format(o))

        proto.write(ResponseReadObject(self.id_, o, self.message_id))

class ResponseReadObject(Packet):
    def __init__(self, id_, o, response_to):
        self.id_ = id_
        self.o = o
        self.response_to = response_to

class WriteBinary(Packet):
    def __init__(self, id_, o):
        self.id_ = id_
        self.o = o

    async def __call__(self, proto):
        logger.debug('{} call'.format(self.__class__.__name__))

        proto.app.write_binary(self.id_, self.o)

class ReadBinary(Packet):
    def __init__(self, id_):
        self.id_ = id_

    async def __call__(self, proto):
        logger.debug('{} call'.format(self.__class__.__name__))

        b = await proto.app.read_binary(self.id_)

        logger.debug('b={}'.format(b))

        proto.write(ResponseReadBinary(self.id_, b, self.message_id))

class ResponseReadBinary(Packet):
    def __init__(self, id_, b, response_to):
        self.id_ = id_
        self.b = b
        self.response_to = response_to

