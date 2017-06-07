""" Resource access functions. """

import asyncio

from . import message
from . import base_resource
from . import resources
from . import nodes
from .util import logger


@asyncio.coroutine
def get_nodeaddr(nodename):
    try:
        ntries = 2;
        iter = 0;
        me = nodes.self_node()
        while (iter <= ntries):
            node = nodes.lookup_remote_node(nodename)
            if (node != None and node.addr != ""):
                return node.addr
            yield from broadcast("Node_Query", nodename, me.name)
            yield from asyncio.sleep(0.5, loop=me.event_loop())
            iter = iter + 1
            
        if (node == None):
            raise Exception("get_nodeaddr: Unknown node")
            
        if (node.addr == ""):
            raise Exception("get_nodeaddr: Node address not known")

    except Exception as e:
        raise e


@asyncio.coroutine
def call(nodename, resource, *args):
    """ 
    Access the resource with the given arguments. 
    To access a local resource, use "." as the nodename. 
    """
    try:
        me = nodes.self_node()
        logger.debug("FUNCCALL(%s, %s)" % (nodename, resource))
        if (nodename == "."):
            destaddr = me.addr
        else:
            destaddr = yield from get_nodeaddr(nodename)

        m = message.create(message.MESG_CALL,
                           me.addr, destaddr,
                           resource, *args)
        result = yield from me.dispatcher.send(m)
        retvals, *rest = result
        return retvals

    except Exception as e:
        raise e


@asyncio.coroutine
def callnr(nodename, resource, *args):
    """ 
    Access the resource with the given arguments. 
    To access a local resource, use "." as the nodename. 
    """
    try:
        me = nodes.self_node()
        if (nodename == "."):
            destaddr = me.addr
        else:
            destaddr = yield from get_nodeaddr(nodename)

        m = message.create(message.MESG_CALL,
                           me.addr, destaddr,
                           resource, *args)
        m.set_noret(1)
        yield from me.dispatcher.send(m)
        
        return

    except Exception as e:
        raise e

    
@asyncio.coroutine
def broadcast(resource, *args):
    """ 
    Access the resource on all local network.
    """
    try:
        logger.debug("BROADCAST(%s)" % (resource))
        me = nodes.self_node()
        m = message.create(message.MESG_BCAST,
                           me.addr, "",
                           resource, *args)
        m.set_noret(1)
        yield from me.dispatcher.send(m)
        
    except Exception as e:
        raise e

@asyncio.coroutine
def _subscribe(nodename, eventname):
    """
    Subscribes to the specified event on remote node.
    """
    try:
        logger.debug("SUBSCRIBE(%s, %s)" % (nodename, eventname)) 
        me = nodes.self_node()
        if (nodename == "."):
            destaddr = me.addr
            nodename = me.name
        else:
            destaddr = yield from get_nodeaddr(nodename)

        eventkey = nodename + ":" + eventname
        pev = base_resource.lookup_resource(eventkey)
        if (pev == None):
            pev = resources.ProxyEvent(eventkey, me.event_loop())
            base_resource.add_resource(eventkey, pev)
        else:
            return pev

        callargs = [ me.name ]
        m = message.create(message.MESG_CALL,
                           me.addr, destaddr,
                           eventname, *callargs)
        m.set_noret(1)
        yield from me.dispatcher.send(m)
        return pev
        
    except Exception as e:
        raise e


@asyncio.coroutine
def waitfor(nodename, eventname):
    """
    Wait for the given remote event. Returns with the value of an event 
    occurrence.
    """
    try:
        pev = yield from _subscribe(nodename, eventname)
        value = yield from pev.wait()
        return value

    except Exception as e:
        raise e

@asyncio.coroutine
def fire(eventname, value):
    """
    Generates an event instances with optional value.
    """
    try:
        ev = base_resource.lookup_resource(eventname)
        if (ev == None):
            raise Exception("No such event: %s" % eventname)

        eventkey = nodes.self_node().name + ":" + eventname
        callargs = [ value ]
        for sub in ev.subs:
            yield from callnr(sub, eventkey, *callargs)

    except Exception as e:
        raise e

