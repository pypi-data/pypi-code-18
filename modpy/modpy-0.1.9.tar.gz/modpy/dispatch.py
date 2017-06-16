""" ModRPC runtime. """

import sys
import asyncio
import logging

from . import message
from . import base_resource
from .rpc_client import CallClient, Call
from .rpc_server import CallServer
from .util import logger


class Dispatcher:
    """
    """
    loop = None
    input_queue = None
    output_queue = None
    rpc_server = None
    rpc_client = None

    def __init__(self, name, selfaddr, rpc_port, mcast_ipaddr, mcast_port, loop=None):
        self.name = name
        self.addr = selfaddr
        self.rpc_port = rpc_port
        self.mcast_ipaddr = mcast_ipaddr
        self.mcast_port = mcast_port

        if sys.platform == "win32" or sys.platform == "cygwin":
            self.loop = loop or asyncio.ProactorEventLoop()
        elif sys.platform == "linux2":
            self.loop = loop or asyncio.SelectorEventLoop()
        else:
            self.loop = loop or asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.codec = message.MessageCodecJSON()

        self.rpc_server = CallServer(self.codec, self.rpc_port,
                                     self.mcast_port, self.addr,
                                     self.input_queue, self.output_queue,
                                     self.loop)
        
        self.rpc_client = CallClient(self.codec, self.rpc_port,
                                     self.mcast_ipaddr, self.mcast_port,
                                     self.addr,
                                     self.input_queue, self.output_queue,
                                     self.loop)
        
        self.dispatcher = self.loop.create_task(self.dispatch_coro())

        self.initials = self.initials_coro()


    def start(self):
        self.loop.run_until_complete(
            asyncio.gather(self.rpc_server.recv_coro,   # receiver
                           self.rpc_server.mcast_coro,  # mcaster
                           self.rpc_client.send_coro(), # sender
                           self.dispatcher,             # dispatcher
                           self.initials,
                           loop=self.loop))
        
    def stop(self):
        try:
            future = asyncio.run_coroutine_threadsafe(self.shutdown_coro(),
                                                      self.loop)
            future.result(timeout=60)
        except Exception as e:
            print(e)
        return

    @asyncio.coroutine
    def initials_coro(self):
        # XXX: wait for 0.5sec until send/recv/dispatch coroutines
        # are up -- find a better way to schedule initials after them
        try:
            yield from asyncio.sleep(0.5, loop=self.loop)

            m = message.create(message.MESG_CALL, self.addr, self.addr,
                               "SYS_INITIAL", )
            m.set_noret(1)
            #self.input_queue.put_nowait(m)
            yield from self.send(m)
        except Exception as e:
            print("SYS_INTIIAL:", e)
            
        return

    @asyncio.coroutine
    def shutdown_coro(self):
        m = message.create(message.MESG_CALL, self.addr, self.addr,
                           "SYS_FINAL", )
        yield from self.send(m)

        self.input_queue.put_nowait(message.IMESG_SHUTDOWN)
        self.output_queue.put_nowait(message.IMESG_SHUTDOWN)
        self.rpc_server.recv_coro.close()
        self.rpc_server.mcast_coro.close()
        self.initials.close()

        return

    """
    Functions for handling incoming requests.
    """
    @asyncio.coroutine
    def dispatch_coro(self):
        """ Input message dispatcher. """

        while True:
            m = yield from self.input_queue.get()
            logger.debug("[DISPATCH]: " + str(m))
            if (m == message.IMESG_SHUTDOWN):
                print("Closing dispatcher...")
                return
            
            if (m.body.tag == message.MESG_CALL):
                if (m.is_noret()):
                    asyncio.ensure_future(self.execute_nb_coro(m), loop=self.loop)
                else:
                    asyncio.ensure_future(self.execute_coro(m), loop=self.loop)
            elif (m.body.tag == message.MESG_BCAST):
                asyncio.ensure_future(self.execute_nb_coro(m), loop=self.loop)
            elif (m.body.tag == message.MESG_RETURN):
                asyncio.ensure_future(self.return_coro(m), loop=self.loop)
            else:
                print("Invalid message tag:", str(m))


    @asyncio.coroutine
    def execute_coro(self, m):
        """ Execute CALL message. """
        try:
            res = base_resource.lookup_resource(m.body.resource)
            if (res == None):
                logger.log(logging.INFO, "No such resource: %s", m.body.resource)
                m = message.create(message.MESG_RETURN,
                                   self.addr, m.header.srcaddr,
                                   message.RESULT_ERROR,
                                   "NoSuchResource")
                self.output_queue.put_nowait(m)
            else:
                logger.debug("[EXEC] Start: %r (%r)" % (res.name, m.body.args))
                callid = m.header.callid
                ret = yield from res.call(*m.body.args)
                m = message.create(message.MESG_RETURN,
                                   self.addr, m.header.srcaddr,
                                   message.RESULT_OK, ret)
                m.header.callid = callid
                self.output_queue.put_nowait(m)
                logger.debug("[EXEC] Done: %s" % str(m))

        except TypeError as e:
            callid = m.header.callid
            m = message.create(message.MESG_RETURN,
                               self.addr, m.header.srcaddr,
                               message.RESULT_ERROR, message.ERROR_TYPE)
            m.header.callid = callid
            self.output_queue.put_nowait(m)

        except Exception as e:
            m = message.create(message.MESG_RETURN,
                               self.addr, m.header.srcaddr,
                               message.RESULT_ERROR, str(e))
            callid = m.header.callid
            self.output_queue.put_nowait(m)

    @asyncio.coroutine
    def execute_nb_coro(self, m):
        """ Execute CALL message which does not require return. """
        try:
            res = base_resource.lookup_resource(m.body.resource)
            if (res == None):
                logger.log(logging.INFO, "No such resource: %s", m.body.resource)

            else:
                logger.debug("[EXECNB] Start: %r (%r)" % (res, m.body.args))
                callid = m.header.callid
                yield from res.call(*m.body.args)
                logger.debug("[EXECNB] Done:")

        except TypeError as e:
            print("Exception:", e)
            callid = m.header.callid
            m = message.create(message.MESG_RETURN,
                               self.addr, m.header.srcaddr,
                               message.RESULT_ERROR, message.ERROR_TYPE)
            m.header.callid = callid
            self.output_queue.put_nowait(m)

        except Exception as e:
            print("Exception:", e)
            m = message.create(message.MESG_RETURN,
                               self.addr, m.header.srcaddr,
                               message.RESULT_ERROR, str(e))
            callid = m.header.callid
            self.output_queue.put_nowait(m)
            
    @asyncio.coroutine
    def return_coro(self, m):
        """ Execute RETURN message. """
        try:
            logger.debug("[RETURN] Start(cid=%d): %s" % (m.header.callid, str(m)))
            c = self.rpc_client.callmap[m.header.callid]
            yield from c.queue.put(m.body.args)
            logger.debug("[RETURN] Done")
        except Exception as e:
            logger.log(logging.INFO, "Exception: %r", e)


    """
    Functions for sending outgoing requests.
    """
    @asyncio.coroutine
    def call_coro(self, m):
        try:
            c = Call(m, self.loop)
            m.header.callid = self.rpc_client.callseq
            logger.debug("[CALL] START callid: %d" % m.header.callid)

            self.rpc_client.callmap[self.rpc_client.callseq] = c
            self.rpc_client.callseq = self.rpc_client.callseq + 1
            
            self.output_queue.put_nowait(m)

            if (not m.is_noret()):
                result = yield from c.queue.get()
                logger.debug("[CALL] Result(cid=%d): %r" % (m.header.callid, result))
                return result

        except Exception as e:
            logger.debug("[CALL] Exception: %r" % e)
            return 123

    @asyncio.coroutine
    def send(self, m):
        """ 
        Blocking function call,
        """
        try:
            call_task = asyncio.ensure_future(self.call_coro(m), loop=self.loop)
            result = yield from asyncio.wait_for(call_task, loop=self.loop, timeout=None)
            return result
            
        except Exception as e:
            logger.log(logging.INFO, "Exception: %r" % e)
            return None

            

