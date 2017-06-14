#Created by Yitong Song in May, 2017
from project_deployer import *

class Job:
	# build the types of commands
	global types 
	cmd_types = ["command", "java", "javaprocess", "pig"]
	types = {}
	for cmd in cmd_types:
		types[cmd] = cmd


	#constructor
	def __init__(self, name, options):
		try:
			options
		except NameError:
			self.options = {}
		else:
			self.options = options

		if "type" not in self.options:
			self.options["type"] = types["command"]
		self.name = name
		self.types = types
		

	#*************************************************************************#
	#Merge the key and the value in a dict to a string in a certain form      #
	#@params:                                                                 #
	#   - self: a Job object                                                  #
	#@return: 																  #
	#	- serialized: a string made up with k and v in a certain form         #
	#*************************************************************************#
	def serialize(self):
		serialized = ""
		for k in self.options.keys():
			if self.options[k] is None:
				serialized += process_property(k,"")
			else:
				serialized += process_property(k,self.options[k])
		return serialized



