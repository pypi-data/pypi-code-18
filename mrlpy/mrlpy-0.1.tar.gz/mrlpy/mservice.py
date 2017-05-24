import mcommand

class MService (object):
	name = ""	

	def __init__(self, name):
		self.name = name
		mcommand.sendCommand("runtime", "registerService", [self.name])
		mcommand.addEventListener(self.name, self.onEvent)

	def onEvent(self, e):
		#Invoke method with data
		params = ','.join(map(str, e.data))
		eval(e.method + '(' + params + ')')
	def __del__(self):
		mcommand.sendCommand("runtime", "deregisterService", [self.name])
		mcommand.removeEventListener(self.name, self.onEvent)
