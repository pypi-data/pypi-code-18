""" Node management. """

import sys
import argparse
import asyncio
import socket
import atexit

from . import util
from . import dispatch

DEFAULT_RPC_PORT = 12345
DEFAULT_MCAST_PORT = 5432
DEFAULT_MCAST_IPADDR = "224.0.0.251"
DEFAULT_MODRPC_DIR = "opt/modrpc"

class NodeBase:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr

    def get_addr():
        return addr

class Node(NodeBase):
    """ Node that represents the self node. """
    name = ""
    runtime = None
    
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--name", type=str, action="store",
                            dest="name", default=sys.argv[0],
                            help="Set the name of node.")
        parser.add_argument("--rpcport", type=int, action="store",
                            dest="rpcport",
                            default=DEFAULT_RPC_PORT,
                            help="Set RPC port.")
        parser.add_argument("--mcastip", type=str, action="store",
                            dest="mcastipaddr",
                            default=DEFAULT_MCAST_IPADDR,
                            help="Set multicast IP address.")
        parser.add_argument("--mcastport", type=int, action="store",
                            dest="mcastport",
                            default=DEFAULT_MCAST_PORT,
                            help="Set multicast port.")
        parser.add_argument("--debug", action="store_true",
                            dest="debug", default=False,
                            help="Print debug messages.")
        results = parser.parse_args()
        self.name = results.name
        self.rpcport = results.rpcport
        self.mcastipaddr = results.mcastipaddr
        self.mcastport = results.mcastport
        self.debug = results.debug

        self.hostname = socket.gethostname()
        self.ipaddr = util.get_outbound_ip()
        self.addr = self.ipaddr + ":" + str(self.rpcport)

        self.dispatcher = dispatch.Dispatcher(self.name, self.addr,
                                              self.rpcport, self.mcastipaddr,
                                              self.mcastport)
        self.loop = self.dispatcher.loop

    def event_loop(self):
        return self.loop

    def start(self):
        self.dispatcher.start()

    def stop(self):
        self.dispatcher.stop()

        
class RemoteNode(NodeBase):
    def __init__(self, name):
        NodeBase.__init__(self, name, "")


_node = None
def init_node():
    """ Initialize the node. """
    global _node
    if (_node != None):
        print("Node already initialized...")
        return _node

    _node = Node()
    print("Node initialized (Name=%s, RPC=%s:%d, MCAST=%s:%d)..."
          % (_node.name, _node.ipaddr, _node.rpcport, _node.ipaddr,
             _node.mcastport))
    return _node

@atexit.register
def stop_node():
    if (_node != None):
        _node.stop()

def self_node():
    if (_node == None):
        raise Exception("Node not initialized")
    return _node

def self_nodename():
    if (_node == None):
        raise Exception("Node not initialized")
    return _node.name

def self_nodeaddr():
    if (_node == None):
        raise Exception("Node not initialized")
    return _node.addr
                                
"""
Remote node address Table.
"""
NODESTAT_INIT = 0
NODESTAT_ADDR = 1
NODESTAT_CONN = 2

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
        print("Added node: %s..." % name)

def remove_remote_node(name):
    if (lookup_remote_node(name) != None):
        _nodetab.pop(name, None)
        print("Removed node: %s..." % name)
        
