#!/usr/bin/python

''' Created on May 17, 2017

This module represents the low-level command API
for a running MRL instance.
                ############                     
                ERROR CODES
        0: Success
        1: Incorrect usage from command line
        2: Unable to connect to MRL instance

  sendCommandQuick() and sendCommand()
        return all codes except 1


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
import requests

from mrlpy.meventdispatch import MEventDispatch
from mrlpy.mevent import MEvent
from mrlpy.mrlmessage import MrlMessage
from mrlpy import mproxygen



MRL_URL = "localhost"
MRL_PORT = '8888'

eventDispatch = MEventDispatch()
socket = None
logging.basicConfig()


def sendCommand(name, method, dat):
    '''
    Sends a command to MRL
    
    Initializes socket so that the connection is held;
    Equivalent to sendCommandQuick() if socket has  
    already been initialized   
    '''

    global MRL_URL
    global MRL_PORT
    global socket
    if socket == None:
        socket = websocket.WebSocketApp("ws://" + MRL_URL + ':' + MRL_PORT + '/api/messages',
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
        socket.on_open = on_open
        wst = threading.Thread(target=socket.run_forever)
        wst.daemon=True
        wst.start()
        conn_timeout = 5
        if socket == None or socket.sock == None:
            return 2
        try:
            while not socket.sock.connected and conn_timeout:
                sleep(1)
                conn_timeout -= 1
        except Exception:
            return 2
        return sendCommandQuick(name, method, dat)

   
def sendCommandQuick(name, method, dat):
    '''
    Sends a command to MRL
    
    Sends a command, and if socket is not
    initialized, will create a quick
    connection that bypasses event registers
    '''


    global MRL_URL
    global MRL_PORT
    global socket
    if socket == None:
        try :
            socket = websocket.create_connection("ws://" + MRL_URL + ':' + MRL_PORT + '/api/messages')
        except Exception:
            print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
            return 2
    req = '{"name": ' + name + ', "method": ' + method + ', "data": ' + str(dat) + '}'
    ret = socket.send(req)
    return ret

def callServiceWithJson(name, method, dat):
    '''
    Calls a service's method with data as params.
    
    Returns json
    '''

    global MRL_URL
    global MRL_PORT
    #try :
    #TODO: convert dat to json and MAKE SURE strings include quotes
    datFormed = map((lambda x: '\'' + x + '\'' if isinstance(x, basestring) else x), dat)
    params = json.dumps(datFormed)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.post("http://" + MRL_URL + ':' + MRL_PORT + "/api/services/" + name + '/' + method, data=params, headers=headers)
    #   print "MRL is not online for url " + MRL_URL + ":" + MRL_PORT
    #    return 2
    try:
    	return r.json()
    except Exception:
    	return r.text
    
def callService(name, method, dat):
    '''
    Calls a service's methods with data as params.
    
    Returns what the method returns, and creates a proxy service if service returned.
    '''


    retFromMRL = callServiceWithJson(name, method, dat)
    if isinstance(retFromMRL, basestring):
	return callServiceWithJson(name, method, dat)
    else:
	if 'serviceType' in retFromMRL:
		return mproxygen.genProxy(callServiceWithJson(name, method, dat))
	else:
		return retFromMRL


def callServiceWithVarArgs(*args):
    '''
    Same as callService() except data doesn't have to be in a list
    
    Returns what callService() returns
    '''

    name = args[0]
    method = args[1]
    dat = list(args)[2:]
    return callService(name, method, dat)


def send(dat):
    '''
    Send string to MRL (INTERNAL USE ONLY!)
    '''

    global socket
    try:
        ret = socket.send(dat)
        return ret
    except Exception:
        print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
        return 2



def setURL(url):
    '''
    Self-explanatory
    '''
    global MRL_URL
    MRL_URL = url
    

def setPort(port):
    '''
    Self-explanatory
    '''
    global MRL_PORT
    MRL_PORT = port


###################################
#    START EVENT REGISTERS        #
###################################



def on_error(ws, error):
    '''
    Error event register; called    
    by socket on errors 
    '''
    print(error)



def on_close(ws):
    '''
    Called by socket on closing
    '''
    print("### Closed socket ###")


def on_open(ws):
    '''
    Called by socket when opening
    '''
    print("### Opened socket ###")



def close():
    '''
    Utility function for forcefully closing the connection
    '''

    global socket
    socket.close()


def addEventListener(name, l):
    '''
    Add a listener to topic (name); Normally
    used for registering a service's name to the
    event registers
    '''
    #print "Adding event listener: name=" + name + ", l=" + str(l)
    eventDispatch.add_event_listener(name, l)


def removeEventListener(name, l):
    '''
    Removes listener l from topic name
    '''
    eventDispatch.remove_event_listener(name, l)


def hasEventListener(name, l):
    '''
    Returns true if l is a listener for topic name, false otherwise.
    '''

    return eventDispatch.has_listener(name, l)


def on_message(ws, msg):
    '''
    Primary event register. Everything goes through here
    
    Parses message. If a heartbeat, updates heartbeat register.
    Else, create mrlMessage and dispatch.
    '''

    try:
        msgJson = json.loads(msg)
    except ValueError:
        print "Heartbeat received. WARNING: NOT IMPLEMENTED YET"
        return
    try:
        mrlMessage = MrlMessage(msgJson['name'], msgJson['method'], msgJson['data'])
    except Exception:
        mrlMessage = MrlMessage(msgJson['name'], msgJson['method'], None)

    eventDispatch.dispatch_event(mrlMessage)



################################
#      END EVENT REGISTERS     #
################################




def __del__(self):
    '''
    Releases all proxy services on delete.
    '''

    for type, serv in eventDispatch._events.iteritems():
        self.sendCommand("runtime", "release", [serv.name])



if __name__ == "__main__":
    MRL_URL = os.getenv('MRL_URL', 'localhost')
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

