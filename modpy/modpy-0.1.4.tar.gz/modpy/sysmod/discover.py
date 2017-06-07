import modpy

@modpy.func
def Node_Query(name, requestnode):
    me = modpy.self_node()
    if (me.name == name):
        yield from modpy.callnr(requestnode, "Node_Update", me.name, me.addr)
    return

@modpy.func
def Node_Update(name, addr):
    node = modpy.lookup_remote_node(name)
    if (node == None):
        node = modpy.create_remote_node(name)
        modpy.add_remote_node(name, node)
        node.addr = addr
        node.stat = modpy.NODESTAT_INIT
    else:
        if (addr == "."):
            modpy.remove_remote_node(name)
        else:
            node.addr = addr
            node.stat = modpy.NODESTAT_CONN
            
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
