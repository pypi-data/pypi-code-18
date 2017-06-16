import asyncio
import modpy
import time

NODESTAT_INIT = 0
NODESTAT_CONN = 1

HEARTBEAT_PERIOD = 60

class RemoteNode:
    def __init__(self, name):
        self.name = name
        self.addr = ""
        self.status = NODESTAT_INIT
        self.lastupdate = time.time()

    def set_addr(self, addr):
        self.addr = addr
        
    def set_status(self, status):
        self.status = status
        self.lastupdate = time.time()

    def get_status(self):
        return self.status

    def sincelast(self):
        return time.time() - self.lastupdate

_nodetab = {}

def create_remote_node(name):
    return RemoteNode(name)

def lookup_remote_node(name):
    if name in _nodetab.keys():
        return _nodetab[name]
    else:
        return None

def add_remote_node(name, node):
    if (lookup_remote_node(name) == None):
        _nodetab[name] = node
        #print("Added node: %s..." % name)

def remove_remote_node(name):
    if (lookup_remote_node(name) != None):
        _nodetab.pop(name, None)
        #print("Removed node: %s..." % name)

@modpy.func
def Node_Lookup(name):
    try:
        if (name == "."):
            return modpy.self_nodeaddr()
        
        ntries = 2;
        iter = 0;
        me = modpy.self_node()
        while (iter <= ntries):
            node = lookup_remote_node(name)
            if (node != None):
                print ("NODE.sincelast() == ", node.sincelast())
            if (node != None and node.addr != "" and
                node.sincelast() < (HEARTBEAT_PERIOD * 1.5)):
                return node.addr
            
            yield from modpy.broadcast("Node_Query", name, me.name, me.addr)
            yield from asyncio.sleep(0.5, loop=me.event_loop())
            iter = iter + 1
            
        if (node == None):
            raise Exception("get_nodeaddr: Unknown node")
            
        if (node.addr == ""):
            raise Exception("get_nodeaddr: Node address not known")

    except Exception as e:
        raise e
    
        
@modpy.func
def Node_Query(name, reqnode, reqaddr):
    me = modpy.self_node()
    yield from Node_Update(reqnode, reqaddr)
    if (me.name == name):
        yield from modpy.callnr("%s/Node_Update" % reqnode, me.name, me.addr)
    return


@modpy.func
def Node_Update(name, addr):
    node = lookup_remote_node(name)
    if (node == None):
        node = create_remote_node(name)
        add_remote_node(name, node)
        node.addr = addr
        node.set_status(NODESTAT_CONN)

    else:
        if (addr == "."):
            remove_remote_node(name)
        else:
            node.set_addr(addr)
            node.set_status(NODESTAT_CONN)

@modpy.initial
def Node_Heartbeat():
    me = modpy.self_node()
    while True:
        yield from modpy.broadcast("Node_Update", me.name, me.addr)
        yield from asyncio.sleep(HEARTBEAT_PERIOD, loop=me.event_loop())

@modpy.initial
def Node_Onboard():
    me = modpy.self_node()
    yield from modpy.broadcast("Node_Update", me.name, me.addr)
    return

@modpy.final
def Node_Offboard():
    me = modpy.self_node()
    yield from modpy.broadcast("Node_Update", me.name, ".")
    return

