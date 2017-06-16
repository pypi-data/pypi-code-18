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
RES_REMOTE      = 7
RES_PROXY_EVENT = 8


class Func(Resource):
    """ Represents a function. """
    
    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_FUNC, handler)

    def __str__(self):
        return "Func[%s]" % (self.name)

    
class Initial(Resource):
    """ 
    Represents a initial function, which is executed only once 
    when the node starts. 
    """
    
    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_INITIAL, handler)

    def __str__(self):
        return "Initial[%s]" % (self.name)

class Final(Resource):
    """ 
    Represents a final function, which is executed only once 
    when the node stops. 
    """

    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_FINAL, handler)

    def __str__(self):
        return "Initial[%s]" % (self.name)
    

class Event(Resource):
    """ Represents an event. """

    def __init__(self, name, handler):
        Resource.__init__(self, name, RES_EVENT, handler)
        self.subs = set()

    def add_subscriber(self, node):
        # XXX: skip redundant sub
        if (not node in self.subs):
            self.subs.add(node)

    def __str__(self):
        return "Event[%s]" % (self.name)

class ProxyEvent(Resource):
    """ Proxy to a remote event. """

    @asyncio.coroutine
    def trigger(self, value):
        for dependent in self.dependents:
            dependent.set_done(self)
        self.queue.put_nowait(value)

    def __init__(self, eventkey, loop):
        Resource.__init__(self, eventkey, RES_PROXY_EVENT, self.trigger)
        self.eventkey = eventkey
        self.queue = asyncio.Queue(loop=loop)
        self.dependents = set()

    @asyncio.coroutine
    # what if there are multiple subscribers to the same remote event
    # in the local node. i.e. multiple watiers -- need one queue per
    # subscriber in the node
    def wait(self):
        value = yield from self.queue.get()
        return value

    def add_dependent(self, evset):
        self.dependents.add(evset)
        
    def remove_dependent(self, evset):
        self.dependents.remove(evset)
        
    def __str__(self):
        return "ProxyEvent[%s]" % (self.eventkey)

    
    
class ProxyEventSet:
    def __init__(self):
        self.pevs = {}
        self.ndone = 0
        self.invalid = False
        self.queue = asyncio.Queue()

    def add_pev(self, pev):
        self.pevs[pev] = False # not fired yet
        self.ndone = self.ndone + 1

    def wait(self):
        self.ndone = len(self.pevs)
        yield from self.queue.get()

    def set_done(self, pev):
        if (self.invalid == True):
            return
        if (pev in self.pevs.keys()):
            if (self.pevs[pev] == False):
                self.pevs[pev] = True
                self.ndone = self.ndone - 1
            
        if (self.ndone == 0):
            self.queue.put_nowait(True)
            self.invalid = True

class Proc(Resource):
    """
    Process is a code which can be started, suspended, resumed, and killed.
    """
    def __init__(self, name, body):
        Resource.__init__(self, name, RES_PROC, body)
        self.task = None
        # XXX: check if 1)  body does not contain any for loop, and
        # 2) it contains a wait statement

    @asyncio.coroutine
    def start(self):
        if (self.task == None):
            self.task = self.loop.create_task(self.handler())
        return
        
    @asyncio.coroutine
    def stop(self):
        self.task.cancel()
        self.task = None
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
Resource factory
"""
def create_event(name):
    ev = Event(name, None)
    add_resource(name, ev)
    
        
"""
Built-in system resources.
"""

_inittasks = []

@func
def SYS_INITIAL():
    """ Called by te dispatcher once after dispatcher starts. """
    import modpy
    loop = modpy.self_node().event_loop()
    global _inittasks
    for key, res in restab.items():
        if (res.typ == RES_INITIAL):
            print("@modpy.initial: %s..." % res.name)
            task = loop.create_task(res.call())
            _inittasks.append(task)
    return
    
    
@func
def SYS_FINAL():
    # cancel any initial tasks still running (e.g. heartbeat)
    for inittask in _inittasks:
        inittask.cancel()

    import modpy
    loop = modpy.self_node().event_loop()
    for key, res in restab.items():
        if (res.typ == RES_FINAL):
            print("@modpy.final: %s..." % res.name)
            #task = yield from res.call()
            task = loop.create_task(res.call())
    return


@func
def SYS_SHUTDOWN():
    import modpy
    me = modpy.self_node()
    me.loop.create_task(me.dispatcher.shutdown_coro())
    return



