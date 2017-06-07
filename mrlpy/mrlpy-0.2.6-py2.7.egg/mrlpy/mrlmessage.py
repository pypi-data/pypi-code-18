from mevent import MEvent

"""Subclass of MEvent, used to represent MRL messages"""
class MrlMessage(MEvent):
	name = ""
	method = ""
	data = []	

	def __init__(self, name, method, dat):
		print "Creating message structure"
		self.name = name
		print "Name set: " + name
		self.method = method
		print "Method set: " + method
		self.data = dat
		print "Data set" 
		super(MrlMessage, self).__init__(name)
