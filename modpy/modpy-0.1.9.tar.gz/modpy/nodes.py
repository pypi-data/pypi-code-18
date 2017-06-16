""" Node management. """

import sys
import argparse
import asyncio
import socket
import atexit
import threading
import logging
import time

from . import util
from . import dispatch

DEFAULT_RPC_PORT = 12345
DEFAULT_MCAST_PORT = 5432
DEFAULT_MCAST_IPADDR = "224.0.0.251"
DEFAULT_MODRPC_DIR = "opt/modrpc"

NODESTAT_INIT = 0
NODESTAT_CONN = 1

class Node:
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
                            help="Print asyncio debug messages.")
        parser.add_argument("--verbose", action="store_true",
                            dest="verbose", default=False,
                            help="Verbose mode.")

        results = parser.parse_args()
        self.name = results.name
        self.rpcport = results.rpcport
        self.mcastipaddr = results.mcastipaddr
        self.mcastport = results.mcastport
        self.debug = results.debug
        self.verbose = results.verbose

        self.hostname = socket.gethostname()
        self.ipaddr = util.get_outbound_ip()
        self.addr = self.ipaddr + ":" + str(self.rpcport)
        self.status = NODESTAT_CONN

        self.dispatcher = dispatch.Dispatcher(self.name, self.addr,
                                              self.rpcport, self.mcastipaddr,
                                              self.mcastport)
        self.loop = self.dispatcher.loop

        if (self.debug):
            logging.basicConfig(level=logging.DEBUG)

    def event_loop(self):
        return self.loop

    def start(self):
        self.dispatcher.start()

    def stop(self):
        self.dispatcher.stop()

    def thr_start(self):
        thr = threading.Thread(target=start, args=())
        thr.start() 
        
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

def stop_node():
    global _node
    if (_node != None):
        _node.stop()
    _node = None

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
                                
