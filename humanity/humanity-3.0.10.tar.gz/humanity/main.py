#! /usr/bin/env python3
'''Main functions from humanity.
'''

from .indexes import *



def _generate_class_definition (name):
	""" Generates class definition for humlist, humtuple, humstr classes.
	"""
	
	class_definition = """
class hum{name}({name}):
	''' Class, that is the same to {name} type, but with normal indexes.
	revision: 3
	'''
""".format (name=name)
	
	
	
	# General methods (same for humlist, humstr, humtuple):
	
	class_definition += """
	def __getitem__(self, keys):
		''' Is launched when "a[0]".
		'''
		keys = change_indexes_1_to_0(keys)
		return self.__class__.__base__.__getitem__(self, keys)
"""
	
	class_definition += """
	def __setitem__(self, keys, value):
		''' Set self[key] to value. If A = [1,2,3], than A[1] = 5 will change A to: [5,2,3]
		'''
		keys = change_indexes_1_to_0(keys)
		self.__class__.__base__.__setitem__(self, keys, value) # keys - итерируемый объект: (slice(1,2,1), ) или (1, )
"""
	
	class_definition += """
	def __delitem__(self, keys):
		''' Delete self[key]. If A = [1,2,3], than A[1] = 5 will change A so: [5,2,3]''' 
		keys = change_indexes_1_to_0(keys)
		self.__class__.__base__.__delitem__(self, keys)
"""

	class_definition += """
	def get(self, keys):
		'''Get method for sequences.
		Returns value of element on position (keys). If such element is absent - returns None.
		Used in: humlist, humtuple, humstr.
		rev. 1
		'''
		try:
			value = self.__getitem__(keys)
		except (IndexError, KeyError):
			value = None
		return value
"""
	
	class_definition += """
	def index(self, value, *positions):
		'''Index method for sequences.
		Returns index of element with specified value (optional in positions).
		rev. 1
		'''
		
		length = len(positions)
	
		if length >= 3:
			raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
		elif length == 2:
			start = positions[0] - 1
			end = positions[1]
			return self.__class__.__base__.index(self, value, start, end) + 1
		elif length == 1:
			start = positions[0] - 1
			return self.__class__.__base__.index(self, value, start) + 1
		else:  # если нет вообще позиций
			return self.__class__.__base__.index(self, value) + 1
"""
	
	class_definition += """
	def {method}(self, *args):
		''' Method for creating hum{name}. Is launched when:
		a = humlist(1, 2)
		'''	
		
		classname = 'hum{name}'  # because immutable objects's instances don't have self.__class__ before creation
		length = len(args)
		
		if length > 1:
			if classname == 'humstr':
				result = ''
				for some in args:
					result += str(some)
				{retn}{name}.{method}(self, result)  # retn can be "return ", can be absent
			else:
				{retn}{name}.{method}(self, args)
		
		elif length == 1:
			if args[0].__class__ == tuple:
				{retn}{name}.{method}(self, args[0])  # tuple
			else:
				if classname == 'humstr':
					{retn}{name}.{method}(self, args[0])  # one element
				else:
					{retn}{name}.{method}(self, args)  # tuple with one element
		
		else:  # length == 0
			{retn}{name}.{method}(self)""".format (
				name = name,
				method = "__init__" if name == "list" else "__new__",
				retn = "" if name == "list" else "return "
	)  # can be optimized:
	
	
	
	# Class-specific methods:
	
	## For humlist:
	
	insert_definition = """
	def insert(self, position, value):
		position = changeIndexes(position)
		list.insert(self, position, value)
"""
	
	## For humtuple:  absent
	
	## For humstr:
	
	find_definition = """
	def find(self, value):
		result = str.find(self, value)
		if result != -1:
			return result + 1
		else:
			return result
		
"""
	
	rindex_definition = """
	def rindex(self, value, *positions):
		length = len(positions)
	
		if length >= 3:
			raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
		elif length == 2:
			start = positions[0] - 1
			end = positions[1]
			return self.__class__.__base__.rindex(self, value, start, end) + 1
		elif length == 1:
			start = positions[0] - 1
			return self.__class__.__base__.index(self, value, start) + 1
		else:  # если нет вообще позиций
			return self.__class__.__base__.index(self, value) + 1
"""
	
	'''format_definition = """
	def format(self, *args, **kwargs):
		if args:
			return str.format(self, '', *args, **kwargs)
		else:
			return str.format(self, *args, **kwargs)
"""'''  # work on it
	
	
	# let's construct it:
		
	if name == "list":
		class_definition += insert_definition
	
	elif name == "tuple":
		pass
	
	elif name == "str":
		class_definition += find_definition  # rfind works as it is
		class_definition += rindex_definition  # rfind works as it is
		#class_definition += format_definition  # work on it
 
	
	return class_definition




for name in ('list', 'tuple', 'str'):
	exec (_generate_class_definition (name))	

	
	





class humdict(dict):
	'''Same as dict, but with .get() method.
	'''
	
	get = humlist.get  # it's appropriate








def humrange(*n):
	'''Function, that is the same to range() function, but with normal indexes.
	list(humrange(3)) == [1,2,3]; list(humrange(2, 3)) == [2,3]; list(humrange(10, 8, -1)) == [10, 9, 8]
	rev. 2
	'''
	if len(n) >= 4:  # 4 and more arguments
		return range(*n)  # will raise error
		
	elif len(n) == 3:
	
		if n[0] < n[1]:  # straight order
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])  # + и - дают включительность
			
		elif n[0] > n[1]:  # reverse order
			if n[2] >= 0:
				raise ValueError("Step can't be larger or equal to zero while reverse order.")
			return range(n[0], n[1] - 1, n[2])
			
		else:  # equal
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])
		
	elif len(n) == 2:  # if [0] will be larger than [1] >> [], because range(4,4) and range(4,3) >> []
		if n[0] > n[1]:
			raise ValueError("Start value can't be larger than second while straight order (default step == 1).")
		return range(n[0], n[1] + 1)
		
	elif len(n) == 1:
		if n[0] <= 0:
			raise ValueError("Range from 1 to {0} with step == 1 doesn't exist (default step == 1).".format(n))
		return range(1, n[0] + 1)  # если один аргумент

