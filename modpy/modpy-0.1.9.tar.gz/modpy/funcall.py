""" Resource access functions. """

import asyncio

from . import message
from . import base_resource
from . import resources
from . import nodes
from .util import logger


@asyncio.coroutine
def get_destaddr(node):
    if (node == base_resource.NODE_SELF):
        destaddr = nodes.self_nodeaddr()
    #elif (util.is_addr(node)):
    #destaddr = node
    else:
        destaddr = yield from call("Node_Lookup", node)
    if destaddr == "":
       raise Exception("Failed to find addr")
    return destaddr
    

@asyncio.coroutine
def call(uri, *args):
    """ 
    Access the resource with the given arguments. 
    To access a local resource, use "." as the nodename. 
    """
    try:
        resuri = base_resource.ResourceURI(uri)
        node = resuri.get_node()
        resource = resuri.get_resource()
        
        if (nodes.self_node().verbose):
            print("FUNCCALL(%s, %s)" % (node, resource))

        me = nodes.self_node()
        destaddr = yield from get_destaddr(node)
        m = message.create(message.MESG_CALL,
                           me.addr, destaddr,
                           resource, *args)
        result = yield from me.dispatcher.send(m)
        retvals, *rest = result
        return retvals

    except Exception as e:
        raise e


@asyncio.coroutine
def callnr(uri, *args):
    """ 
    Access the resource with the given arguments. 
    To access a local resource, use "." as the nodename. 
    """
    try:
        resuri = base_resource.ResourceURI(uri)
        node = resuri.get_node()
        resource = resuri.get_resource()
        
        if (nodes.self_node().verbose):
            print("FUNCCALLNR(%s, %s)" % (node, resource))

        me = nodes.self_node()
        destaddr = yield from get_destaddr(node)
        m = message.create(message.MESG_CALL,
                           me.addr, destaddr,
                           resource, *args)
        m.set_noret(1)
        yield from me.dispatcher.send(m)
        
        return

    except Exception as e:
        raise e

    
@asyncio.coroutine
def broadcast(uri, *args):
    """ 
    Access the resource on all local network.
    """
    try:
        resuri = base_resource.ResourceURI(uri)
        node = resuri.get_node()
        resource = resuri.get_resource()

        if (nodes.self_node().verbose):
            print("BROADCAST(%s)" % (resource))
        
        me = nodes.self_node()
        m = message.create(message.MESG_BCAST,
                           me.addr, "",
                           resource, *args)
        m.set_noret(1)
        yield from me.dispatcher.send(m)
        
    except Exception as e:
        raise e

@asyncio.coroutine
def _subscribe(uri):
    """
    Subscribes to the specified event on remote node.
    """
    try:
        resuri = base_resource.ResourceURI(uri)
        node = resuri.get_node()
        eventname = resuri.get_resource()

        if (nodes.self_node().verbose):
            print("SUBSCRIBE(%s, %s)" % (node, eventname)) 
        me = nodes.self_node()
        destaddr = yield from get_destaddr(node)
        if (node == base_resource.NODE_SELF):
            nodename = me.name
        else:
            nodename = node

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
def _waitfor(uri):
    """
    Wait for the given remote event. Returns with the value of an event 
    occurrence.
    """
    try:
        pev = yield from _subscribe(uri)
        value = yield from pev.wait()
        return value

    except Exception as e:
        raise e



@asyncio.coroutine
def waitfor(*uris):
    """
    Wait for the given remote event. Returns with the value of an event 
    occurrence.
    """
    try:
        if (len(uris) == 0):
            return None
        elif (len(uris) == 1):
            value = yield from _waitfor(uris[0])
            return value
        else:
            evset = resources.ProxyEventSet()
            pevs = []
            for uri in uris:
                pev = yield from _subscribe(uri)
                pevs.append(pev)
                pev.add_dependent(evset)
                evset.add_pev(pev)

            yield from evset.wait()
            for pev in pevs:
                pev.remove_dependent(evset)

            # TODO: create eventset factory and use pool
            evset = None
            return None

    except Exception as e:
        raise e

    
@asyncio.coroutine
def fire(uri, value):
    """
    Generates an event instances with optional value.
    """
    try:
        resuri = base_resource.ResourceURI(uri)
        node = resuri.get_node()
        eventname = resuri.get_resource()

        if (node != base_resource.NODE_SELF):
            raise Exception("Only local events can be fired")

        if (nodes.self_node().verbose):
            print("FIRE(eventname):", eventname)
        ev = base_resource.lookup_resource(eventname)
        if (ev == None):
            raise Exception("No such event: %s" % eventname)

        eventkey = nodes.self_nodename() + ":" + eventname
        callargs = [ value ]
        for sub in ev.subs:
            if (nodes.self_node().verbose):
                print("FIRE:%s/%s" % (sub, eventkey))
            yield from callnr("%s/%s" % (sub, eventkey), *callargs)

    except Exception as e:
        raise e

