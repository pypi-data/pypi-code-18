""" ModRPC client responsible for sending messages. """

import asyncio

from . import message
from .util import logger
from .util import addr_to_netaddr

class McastClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        #print("Connection Made")
        self.transport = transport
        self.transport.sendto(self.message.encode())
        #self.transport.close()

    def datagram_recieved(self, data, addr):
        print("UDP received:", data)
        self.transport.close()

    def error_received(self, exc):
        print("UDP send error:", exc)

    def connection_lost(self, exc):
        return
        


class Call:
    """
    Represents a single call instance.
    """

    def __init__(self, message, loop):
        self.message = message
        self.queue = asyncio.Queue(loop=loop)
        
    def __repr__(self):
        return "<%s:%s(%r)>" % (self.header.destaddr,
                                self.body.resource,
                                self.body.args)


class CallClient:
    """
    Responsible for taking a message from the output queue and then 
    sending requests to destinations.
    """
    callmap = {}
    callseq = 0 
   
    def __init__(self, codec, tcp_port, mcast_addr, mcast_port, selfaddr,
                 input_queue, output_queue, loop):
        # input_queue is needed for quick return due to connection
        # error or server error
        self.codec = codec
        self.tcp_port = tcp_port
        self.mcast_addr = mcast_addr
        self.mcast_port = mcast_port
        self.addr = selfaddr
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.loop = loop

    @asyncio.coroutine
    def send_coro(self):
        """
        A coroutine which waits for outgoing messages and send them.
        """
        while True:
            m = yield from self.output_queue.get()
            logger.debug("[SEND] Request: %s" % m)
            if (m == message.IMESG_SHUTDOWN):
                print("Closing RPC client...")
                return
            destaddr = m.header.destaddr
            encm = self.codec.encode_message(m)

            if (m.body.tag < message.MESG_BCAST):
                # RPC calls
                try:
                    if (destaddr == self.addr):
                        # local call
                        print("...LOCAL CALL", m.body.tag)
                        yield from self.input_queue.put(m)
                        continue
                    
                    print("...TCP CALL", m.body.tag)
                    netaddr = addr_to_netaddr(destaddr)
                    ip = netaddr.ipaddr
                    port = netaddr.port
                    reader, writer = yield from \
                        asyncio.open_connection(ip, port, loop=self.loop)
                except Exception as e:
                    print("Connection failed: dest=%s" % (destaddr), str(e))
                    r = message.create(message.MESG_RETURN,
                                       m.header.destaddr,
                                       m.header.srcaddr,
                                       message.RESULT_ERROR,
                                       message.ERROR_CONNFAIL)
                    r.header.callid = m.header.callid
                    yield from self.input_queue.put(r)
                    #if (not writer.is_closing()):
                    #    writer.close()
                    continue

                try: 
                    writer.write(encm.encode())
                    reply = yield from reader.read(100)
                    writer.close()

                except Exception as e:
                    print("No ACK: dest=%s" % (destaddr), str(e))
                    r = message.create(message.MESG_RETURN,
                                       m.header.destaddr,
                                       m.header.srcaddr,
                                       message.RESULT_ERROR,
                                       message.ERROR_NOACK)
                    r.header.callid = m.header.callid
                    yield from self.input_queue.put(r)
                    #if (not writer.is_closing()):
                    #writer.close()
                    continue
                
            else: 
                # Broadcast (m.body.tag == message.MESG_BCAST)
                try:
                    print("...UDP CALL", m.body.tag)
                    connect = self.loop.create_datagram_endpoint(
                        lambda: McastClientProtocol(encm, self.loop),
                        remote_addr=("224.0.0.251", self.mcast_port))
                    asyncio.ensure_future(connect, loop=self.loop)
                    
                except Exception as e:
                    print("UDP Connection failure: %d" % (self.mcast_port))
                    continue
