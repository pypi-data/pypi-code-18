import asyncio
import logging
import pickle
import io

logger = logging.getLogger(__name__)

class Protocol(asyncio.Protocol):
    def __init__(self, loop):
        logger.debug('Protocol created')
        self.loop = loop
        self.__message_id_last = 0
        self.__message_futures = {}
        self.queue_packet_acall = asyncio.Queue()

    def __next_message_id(self):
        self.__message_id_last += 1
        return self.__message_id_last

    def connection_made(self, transport):
        logger.debug('Connection made')
        logger.debug('transport = {}'.format(transport))
        peername = transport.get_extra_info('peername')
        logger.debug('Connection from {}'.format(peername))
        self.transport = transport
     
    def connection_lost(self, exc):
        logger.debug('The server closed the connection {}'.format(exc))
    
    def data_received(self, data):
        logger.debug('Received {} bytes'.format(len(data)))
        
        try:
            stream = io.BytesIO(data)
            
            while True:
                try:
                    packet = pickle.load(stream)
                except EOFError as e:
                    logger.debug(repr(e))
                    break
                except Exception as e:
                    logger.error(e)
                    raise
            
                if hasattr(packet, 'response_to'):
                    try:
                        future = self.__message_futures[packet.response_to]
                    except Exception as e:
                        logger.error(e)
                    else:
                        future.set_result(packet)
        
                self.packet_received(packet)
        except Exception as e:
            logger.error(str(e))

    def packet_received(self, packet):
        task = self.loop.create_task(packet(self))
        # keep track of packet acall coroutines
        self.queue_packet_acall.put_nowait(task)
        return task

    def write(self, packet):
        """
        assign a message_id 
        """
        packet.message_id = self.__next_message_id()
        b = pickle.dumps(packet)
        self.transport.write(b)
        
        logger.debug('write {} {} bytes'.format(packet.__class__.__name__, len(b)))

        fut = self.loop.create_future()
        self.__message_futures[packet.message_id] = fut
        return fut


