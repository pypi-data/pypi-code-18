#!/usr/bin/python

'''
Created on May 17, 2017

@author: AutonomicPerfectionist
'''
import websocket
import logging
import thread
import time
from time import sleep
import os
import sys
import threading
import json

from meventdispatch import MEventDispatch
from mevent import MEvent
from mrlmessage import MrlMessage
##################################################
#This module represents the low-level command API#
#for a running MRL instance.			 #
#		############			 #
#		ERROR CODES			 #
#	0: Success, shutdown successful		 #
#	1: Incorrect usage from command line	 #
#	2: Unable to connect to MRL instance	 #
#						 #
#  sendCommandRelease() and sendCommandHold()    #
#	return all codes except 1		 #
##################################################

MRL_URL = "ws://localhost"
MRL_PORT = '8888'

eventDispatch = MEventDispatch()
socket = None

####################################################
#Initializes socket so that the connection is held;#
#Equivalent to sendCommandQuick() if socket has    #
#already been initialized                          #
####################################################
def sendCommand(name, method, dat):
    global MRL_URL
    global MRL_PORT
    global socket
    if socket == None:
        socket = websocket.WebSocketApp(MRL_URL + ':' + MRL_PORT + '/api/messages',
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
        socket.on_open = on_open
        wst = threading.Thread(target=socket.run_forever)
        wst.daemon=True
        wst.start()
        conn_timeout = 5
        if socket.sock == None or socket == None:
            return 2
        while not socket.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
    return sendCommandQuick(name, method, dat)

##########################################
#Sends a command, and if socket is not   #
#initialized, will create a quick        #
#connection that bypasses event registers#
#########################################   
def sendCommandQuick(name, method, dat):
    global MRL_URL
    global MRL_PORT
    global socket
    if socket == None:
        try :
            socket = websocket.create_connection(MRL_URL + ':' + MRL_PORT + '/api/messages')
        except Exception:
            print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
            return 2
    req = '{"name": ' + name + ', "method": ' + method + ', "data": ' + str(dat) + '}'
    ret = socket.send(req)
    return ret

def send(dat):
    global socket
    try:
        ret = socket.send(dat)
        return ret
    except Exception:
        print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
        return 2



def setURL(url):
    global MRL_URL
    MRL_URL = url
    
def setPort(port):
    global MRL_PORT
    MRL_PORT = port

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### Closed socket ###")

def on_open(ws):
    print("### Opened socket ###")

def close():
    global socket
    socket.close()

def addEventListener(name, l):
    eventDispatch.add_event_listener(name, l)

def removeEventListener(name, l):
    eventDispatch.remove_event_listener(name, l)
def hasEventListener(name, l):
    return eventDispatch.has_listener(name, l)

def on_message(ws, msg):
    try:
        msgJson = json.loads(msg)
    except ValueError:
        print "Invalid JSON received. Ignoring"
        return
    mrlMessage = MrlMessage(msgJson['name'], msgJson['method'], msgJson['data'])
    eventDispatch.dispatch_event(mrlMessage)

def invokeMsg(msg):
    print "Invoking message on " + str(msg.name) + ", method " + str(msg.method) + ", with dat " + str(msg.dat)

def __del__(self):
    self.sendCommand("runtime", "deregisterServices", [])



if __name__ == "__main__":
    MRL_URL = os.getenv('MRL_URL', 'ws://localhost')
    MRL_PORT = os.getenv('MRL_PORT', '8888')
    logging.basicConfig()
    if len(sys.argv) < 3 :
        print("Usage: mcommand <name> <method> <dat>")
        exit(1)
    #websocket.enableTrace(True)
    ret = sendCommandQuick(sys.argv[1], sys.argv[2], sys.argv[3:])
    
    if ret == 2:
        print("Connection failed.")
        exit(2)        
    print("MRL command sent successfully.")
    close()
    exit(0)

