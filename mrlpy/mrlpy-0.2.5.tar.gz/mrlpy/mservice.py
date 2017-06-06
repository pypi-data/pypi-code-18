global mcommand
global sys
import mcommand
import sys
import time
from mrlpy.exceptions import HandshakeTimeout

"""Represents the base service class"""


class MService (object):
	name = ""	
	handshakeSuccessful = False
	handshakeTimeout = 1
	handshakeSleepPeriod = 0.25
	createProxyOnFailedHandshake = True

	######################################
	#Register service with mcommand event#
	# registers and mrl service registry #
	######################################
	def __init__(self, name=""):
		if name == "":
			#Get name from args
			self.name = sys.argv[2]
		else:
			self.name = name
		self.connectWithProxy(True)

	def connectWithProxy(self, tryagain=False):
		#Can do this since it won't do anything if proxy already active
		mcommand.sendCommand("runtime", "createAndStart", [self.name, "PythonProxy"])
		#Useful for determining whether the proxy service has been created yet
                mrlRet = mcommand.callServiceWithJson(self.name, "handshake", [])

                print "mrlRet = " + str(mrlRet)
                #If we get to here, MRL is running because mcommand did not throw an exception

                #TODO: Use mrlRet to determine if we need to create a proxy service

                #Register this service with MRL's messaging system (Actually, with mcommand's event registers, which forward the event here)
                #Proxy service forwards all messages to mcommand
                mcommand.addEventListener(self.name, self.onEvent)

                #BEGIN HANDSHAKE$
                start = time.time()
                lastTime = 0
                while (not self.handshakeSuccessful) and ((time.time() - start) < self.handshakeTimeout):
                        time.sleep(self.handshakeSleepPeriod)
                        lastTime = time.time()

                #print str(lastTime - start >= self.handshakeTimeout)
                if lastTime - start >= self.handshakeTimeout:
                        if self.createProxyOnFailedHandshake and tryagain:
                                print "Proxy not active. Creating proxy..."
                                mcommand.sendCommand("runtime", "createAndStart", [self.name, "PythonProxy"])
                                self.connectWithProxy()
                        else:   
                                raise HandshakeTimeout("Error attempting to sync with MRL proxy service; Proxy name = " + str(self.name))
                #END HANDSHAKE#

	#########################################
	#Handles message invocation and parsing #
	#of params; WARNING: DO NOT OVERRIDE	#
	#THIS METHOD UNLESS YOU KNOW WHAT YOU	#
	#ARE DOING!!!!!!!			#
	#########################################
	def onEvent(self, e):
		#Enables sending a return value back; Other half implemented in mcommand and proxy service
		ret = None
		#Invoke method with data
		try:
			params = ','.join(map(str, e.data))
			print "Invoking: " + e.method + '(' + params + ')'
			ret = eval('self.' + e.method + '(' + params + ')')
		except Exception:
			print "Invoking: " + e.method + '()'
                        ret = eval('self.' + e.method + '()')
		return ret

	##########################
	#Second half of handshake#
	##########################
	def handshake(self):
		print "Handshake successful."
		self.handshakeSuccessful = True
