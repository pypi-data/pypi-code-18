global mcommand
global sys
import mcommand
import sys


"""Represents the base service class"""

handshake = False

class MService (object):
	name = ""	
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
		mcommand.sendCommand(name, "handshake", [])
		mcommand.addEventListener(self.name, self.onEvent)
		#TODO Wait for handshake#
	#########################################
	#Handles message invocation and parsing #
	#of params				#
	#########################################
	def onEvent(self, e):
		#Invoke method with data
		try:
			params = ','.join(map(str, e.data))
			print "Invoking: " + e.method + '(' + params + ')'
			eval('self.' + e.method + '(' + params + ')')
		except Exception:
			print "Invoking: " + e.method + '()'
                        eval('self.' + e.method + '()')
	##########################
	#Second half of handshake#
	##########################
	def handshake(self):
		global handshake
		print "Handshake successful."
		handshake = True
