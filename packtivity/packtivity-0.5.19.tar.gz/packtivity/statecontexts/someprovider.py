class SharedStateProvider(object):
	def __init__(self):
		pass
	
	def json(self):
		pass

	@classmethod
	def fromJSON(cls,data):
		pass

	def new_state(self, dep_states = None, name = None):
		pass

	def derive(self,name = None):
		'''
		derive a new provider from this one, e.g. by 
		'''
		pass


