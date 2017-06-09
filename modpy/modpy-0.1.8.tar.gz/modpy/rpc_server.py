""" ModRPC server responsible for receiving messages. """

import asyncio
import logging
import socket
import struct
import sys

from .util import logger

class McastServerProtocol(asyncio.Protocol):
    def __init__(self, codec, queue):
        asyncio.Protocol.__init__(self)
        self.codec = codec
        self.input_queue = queue
        
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        m = data.decode()
        #print("UDP received %r from %s" % (m, addr))
        message = self.codec.decode_message(m)
        message.header.source = "%s:%d" % (addr[0], addr[1])
        self.input_queue.put_nowait(message)

class CallServer:
    """
    Responsible for receiving requests and putting them into 
    the input queue.
    """

    def __init__(self, codec, rpc_port, mcast_port, selfaddr,
                 input_queue, output_queue, loop):
        self.codec = codec
        self.rpc_port = rpc_port
        self.mcast_port = mcast_port
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.addr = selfaddr
        self.loop = loop
        self.recv_coro = asyncio.start_server(self.callrecv, None,
                                              self.rpc_port,
                                              loop=self.loop)

        self.reuseport = False
        try:
           socket.So_REUSEPORT 
           self.reuseport = True
        except Exception:
           pass

        try: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            group = socket.inet_aton("224.0.0.251")
            mreq = struct.pack("4sL", group, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if (self.reuseport):
              sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind(("", self.mcast_port))
        except Exception as e:
            print("CallServer failure:", e)
            sys.exit(1)
            
        self.mcast_coro = \
            loop.create_datagram_endpoint(
                lambda: McastServerProtocol(self.codec,
                                            self.input_queue),
                sock=sock)

        logger.log(logging.INFO, "Starting RPC server at port %d",
                   self.rpc_port)
        logger.log(logging.INFO, "Starting MCAST server at port %d",
                   self.mcast_port)

    @asyncio.coroutine
    def callrecv(self, reader, writer):
        try:
            data = yield from reader.read(4096)
            m = data.decode()
            addr, port = writer.get_extra_info("peername")
            logger.debug("[RECV] Message: %s from %r" % (m, addr))
            
            writer.write("ACK".encode())
            yield from writer.drain()
            
            message = self.codec.decode_message(m)
            yield from self.input_queue.put(message)
            writer.close()

        except Exception as e:
            logger.debug("[RECV] Exception: %r", e)
            

            
