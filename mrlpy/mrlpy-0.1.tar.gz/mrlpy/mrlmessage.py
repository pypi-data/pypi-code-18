from mevent import MEvent


class MrlMessage(MEvent):
	name = ""
	method = ""
	data = []	

	def __init__(self, name, method, dat):
		print "Creating message structure"
		self.name = name
		print "Name set"
		self.method = method
		print "Method set"
		self.data = dat
		print "Data set"
		super(MrlMessage, self).__init__(name)

