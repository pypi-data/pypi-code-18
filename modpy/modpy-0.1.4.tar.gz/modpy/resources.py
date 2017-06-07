import functools
import inspect
import asyncio
import sys
import os

from .base_resource import Resource
from .base_resource import add_resource
from .base_resource import restab

"""
Resource types and classses.
"""
RES_PROP        = 0
RES_EVENT       = 1
RES_FUNC        = 2
RES_INITIAL     = 4
RES_FINAL       = 5
RES_PROC        = 6
RES_TIMER       = 7
RES_REMOTE      = 8
RES_PROXY_EVENT = 9
RES_NTYPES      = 10


class Func(Resource):
    """ Represents a function. """
    
    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_FUNC, handler)

    def __str__(self):
        return 'Func[%s]' % (self.name)

    
class Initial(Resource):
    """ 
    Represents a initial function, which is executed only once 
    when the node starts. 
    """
    
    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_INITIAL, handler)

    def __str__(self):
        return 'Initial[%s]' % (self.name)

class Final(Resource):
    """ 
    Represents a final function, which is executed only once 
    when the node stops. 
    """

    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_FINAL, handler)

    def __str__(self):
        return 'Initial[%s]' % (self.name)
    

class Event(Resource):
    """ Represents an event. """

    subs = []
    
    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_EVENT, handler)

    def add_subscriber(self, node):
        # XXX: skip redundant sub
        self.subs.append(node)

    def __str__(self):
        return 'Event[%s]' % (self.name)


class ProxyEvent(Resource):
    """ Proxy to a remote event. """

    queue = None

    @asyncio.coroutine
    def trigger(self, value):
        print("TRIGGER: ", value)
        yield from self.queue.put(value)

    def __init__(self, eventkey, loop):
        Resource.__init__(self, eventkey, RES_PROXY_EVENT, self.trigger)
        self.eventkey = eventkey
        self.queue = asyncio.Queue(loop=loop)

    @asyncio.coroutine
    # what if there are multiple subscribers to the same remote event
    # in the local node. i.e. multiple watiers -- need one queue per
    # subscriber in the node
    def wait(self):
        value = yield from self.queue.get()
        return value
        
    def __str__(self):
        return 'ProxyEvent[%s (%s)]' % (self.nodename, self.eventname)

    
class Proc(Resource):
    """
    Process is a code which can be started, suspended, resumed, and killed.
    """
    def __init__(self, name, body):
        Resource.__init__(self, name, RES_PROC, body)
        self.queue = asyncio.Queue()
        # XXX: check if 1)  body does not contain any for loop, and
        # 2) it contains a wait statement

    @asyncio.coroutine
    def control_loop(self):
        while True:
            cmd = yield from self.queue.get()
            if self.state == STAT_STOPPED:
                if cmd == CMD_RUN:
                    pass
            elif self.state == STAT_RUNNING:
                if cmd == CMD_STOP:
                    pass
            else:
                pass
            
        
    @asyncio.coroutine
    def start(self):
        return
        
    @asyncio.coroutine
    def stop(self):
        return

    @asyncio.coroutine
    def kill(self):
        return
        

"""
Resource decorators.
"""
def func(fn):
    """ Decorator for ModRPC functions. """
    @asyncio.coroutine
    def wrapper(*args):
        w =  fn(*args)
        return w

    name = fn.__name__
    res = Func(name, wrapper)
    add_resource(name, res)
    
    return wrapper

def initial(fn):
    """ Decorator for ModRPC initial functions. """
    @asyncio.coroutine
    def wrapper(*args):
        w =  fn(*args)
        return w

    argspec = inspect.getargspec(fn)
    if (len(argspec[0]) != 0):
        raise Exception("@modpy.final function cannot have arguments.")
        
    name = fn.__name__
    res = Initial(name, wrapper)
    add_resource(name, res)
    
    return wrapper

def final(fn):
    """ Decorator for ModRPC initial functions. """
    @asyncio.coroutine
    def wrapper(*args):
        w =  fn(*args)
        return w

    argspec = inspect.getargspec(fn)
    if (len(argspec[0]) != 0):
        raise Exception("@modpy.final function cannot have arguments.")
        
    name = fn.__name__
    res = Final(name, wrapper)
    add_resource(name, res)
    
    return wrapper


def event(fn):
    """ Decorator for ModRPC events. """

    name = fn.__name__
    ev = Event(name, None)
    add_resource(name, ev)

    #@asyncio.coroutine

    def subs(node):
        ev.add_subscriber(node)
        return []
    
    def wrapper(*args):
        w = subs(*args)
        return w

    argspec = inspect.getargspec(fn)
    if (len(argspec[0]) != 0):
        raise Exception("@modpy.event function cannot have arguments.")
    ev.handler = wrapper

    return wrapper

def timer(fn):
    return 0

def proc(fn):
    """ 
    Decorator for ModRPC processes. A ModRPC process is basically an event loop
    which reacts to event occurrences.
    """

    @asyncio.coroutine
    def wrapper(*args):
        w = fn(*args)
        return w
    
    name = fn.__name__
    res = Resource(name, RES_PROC, wrapper)
    add_resource(name, res)
    
    return wrapper
        
"""
Built-in system resources.
"""
@func
def SYS_INITIAL():
    """ Called by te dispatcher once after dispatcher starts. """
    print("SYS_INIT...")
    for key, res in restab.items():
        if (res.typ == RES_INITIAL):
            yield from res.call()
    return
    
    
@func
def SYS_FINAL():
    print("SYS_FINAL...")
    for key, res in restab.items():
        if (res.typ == RES_FINAL):
            yield from res.call()
    return


