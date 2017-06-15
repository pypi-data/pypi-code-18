import asyncio
import io
import logging
import pickle
import struct

logger = logging.getLogger(__name__)

class Protocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.message_id_last = 0
        self.message_futures = {}

        self.header_format = struct.Struct('<i')

    def next_message_id(self):
        self.message_id_last += 1
        return self.message_id_last

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        logger.debug('Connection from {}'.format(peername))
        self.transport = transport
     
    def connection_lost(self, exc):
        logger.debug('The server closed the connection {}'.format(exc))
 
    def data_received(self, data):
        logger.debug('data received {}'.format(len(data)))

        stream = io.BytesIO(data)
        
        #while True:
        #    l = self.header_format.unpack(stream)
            
        #    stream.read(self.header_format.size)
            
        #    print('l =', l)
    
        while True:
            try:
                packet = pickle.load(stream)
            except EOFError:
                break
            except Exception as e:
                logger.error(e)
                raise
        
            try:
                if hasattr(packet, 'response_to'):
                    fut = self.message_futures[packet.response_to]
                    fut.set_result(packet)
            except Exception as e:
                logger.error(e)
    
            self.packet_received(packet)

    def packet_received(self, packet):
        pass

    def write(self, packet):
        """
        assign a message_id 
        """
        packet.message_id = self.next_message_id()
        
        b = pickle.dumps(packet)
        
        #b = self.header_format.pack(len(b)) + b

        self.transport.write(b)
        
        logger.debug('write {} {} bytes'.format(packet.__class__.__name__, len(b)))

        fut = asyncio.Future()
        self.message_futures[packet.message_id] = fut
        return fut



