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
import requests

from mrlpy.meventdispatch import MEventDispatch
from mrlpy.mevent import MEvent
from mrlpy.mrlmessage import MrlMessage
from mrlpy import mproxygen

##################################################
#This module represents the low-level command API#
#for a running MRL instance.			 #
#		############			 #
#		ERROR CODES			 #
#	0: Success				 #
#	1: Incorrect usage from command line	 #
#	2: Unable to connect to MRL instance	 #
#						 #
#  sendCommandQuick() and sendCommand()	         #
#	return all codes except 1		 #
##################################################

MRL_URL = "localhost"
MRL_PORT = '8888'

eventDispatch = MEventDispatch()
socket = None
logging.basicConfig()
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
            #return 2
            pass
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
            socket = websocket.create_connection("ws://" + MRL_URL + ':' + MRL_PORT + '/api/messages')
        except Exception:
            print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
            return 2
    req = '{"name": ' + name + ', "method": ' + method + ', "data": ' + str(dat) + '}'
    ret = socket.send(req)
    return ret

def callServiceWithJson(name, method, dat):
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
	retFromMRL = callServiceWithJson(name, method, dat)
	if isinstance(retFromMRL, basestring):
		return callServiceWithJson(name, method, dat)
	else:
		if 'serviceType' in retFromMRL:
			return mproxygen.genProxy(callServiceWithJson(name, method, dat))
		else:
			return retFromMRL


def callServiceWithVarArgs(*args):
	name = args[0]
	method = args[1]
	dat = list(args)[2:]
	return callService(name, method, dat)

#####################################
#Send string (internal use only)    #
#####################################
def send(dat):
    global socket
    try:
        ret = socket.send(dat)
        return ret
    except Exception:
        print("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
        return 2


####################################
#Self-explanatory :)               #
####################################
def setURL(url):
    global MRL_URL
    MRL_URL = url
    
####################################
#Self-explanatory :)               #
####################################
def setPort(port):
    global MRL_PORT
    MRL_PORT = port


###################################
#    START EVENT REGISTERS        #
###################################


##################################
#Error event register; called    #
#by socket on errors             #
##################################
def on_error(ws, error):
    print(error)


#################################
#Called by socket on closing    #
#################################
def on_close(ws):
    print("### Closed socket ###")

#################################
#Called by socket when opening  #
#################################
def on_open(ws):
    print("### Opened socket ###")


#################################
#Utility method to forcefully   #
#close the connection; also     #
#releases the proxy services    #
#################################
def close():
    global socket
    socket.close()

###########################
#Add a listener to        #
#topic (name); Normally   #
#used for registering a   #
#service's name to the    #
#event registers          #
###########################
def addEventListener(name, l):
    #print "Adding event listener: name=" + name + ", l=" + str(l)
    eventDispatch.add_event_listener(name, l)

#############################
#Removes l on topic name    #
#############################
def removeEventListener(name, l):
    eventDispatch.remove_event_listener(name, l)

###############################
#Returns true if l is         #
#listener for the topic (name)#
###############################
def hasEventListener(name, l):
    return eventDispatch.has_listener(name, l)

###############################
#Event register; parses string#
#and dispatches message event #
###############################
def on_message(ws, msg):
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



##############################
#Releases proxy service on   #
#delete                      #
##############################
def __del__(self):
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

