from mrlpy.mservice import MService
from org.myrobotlab.service import *

class MCompatibilityService(MService):
	def __init__(self, name=""):
		super(MCompatibilityService, self).__init__(name)

	def runScript(self, scriptFile):
		#Runs a script inside this compat service, allowing full usage of Jython syntax
		Runtime.setCompat(True)
		Runtime.setCompatServiceObject(self)
		execfile(str(scriptFile))

	def subscribe(self):
		#Implements python.subscribe()
		#TODO: Implement
		pass
