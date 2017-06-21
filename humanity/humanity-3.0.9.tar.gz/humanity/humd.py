#! /usr/bin/python3
"""Contains classes to use with decimal stuff.
"""

from .indexes import *
from decimal import Decimal  # for humdrange
from .main import humlist  # for taking method __getitem__




class humdrange():  # not a function because of need .__len__() method
	'''Same as humrange, but including decimal (analog to float) numbers.
	Returns Decimal() numbers.
	rev. 5
	'''
	
	
	def __init__(self, a, b, step, return_type='dec'):
		'''Return type: 'dec' - decimal, 'float' - float, 'str' - string (float, written as string),
		'int' - int.
		rev. 3
		'''
		self.check_type_errors(a, b, step, return_type)
		
		a, b, step = Decimal(a), Decimal(b), Decimal(step)
		
		self.a, self.b, self.step = a, b, step
		self.return_type = return_type
		
		self.check_logic_errors()
		
		self.length = self.__len__()
	
	
	
	
	def check_type_errors(self, a, b, step, return_type):
		'''Is launched from .__init__().
		rev.2
		'''
		# check for float:
		if (a.__class__ == float) or (b.__class__ == float) or (step.__class__ == float):
			raise TypeError('You cannot pass float to humdrange because general float type cannot reproduce all numbers - some of them are changed to other, what causes errors.\nPlease, use Decimal(), int, or float, which is written as string (in quotes).')
		
		# we check a:
		if not ((a.__class__ == int) or (a.__class__ == str) or (a.__class__ == Decimal)):
			raise TypeError('Start value must be int or decimal, written as string, or Decimal.')
		# we check b:
		if not ((b.__class__ == int) or (b.__class__ == str) or (b.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		# we check step:
		if not ((step.__class__ == int) or (step.__class__ == str) or (step.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		
		# we check return_type:
		if not (type(return_type) == str):
			raise TypeError('Return type must be specified with appropriate string.')
	
	
	
	
	def check_logic_errors(self):
		'''Checks current instance of humdrange for errors.
		Is launched from .__init__().
		rev. 1
		'''
		# we check step
		if self.step == 0:
			raise ValueError("Step can't be equal to zero.")
		
		# we check a and b depening order
		if self.step < 0:  # reverse order
			if self.a < self.b:
				raise ValueError("Start value ({0}) can't be lesser stop ({1}) while reverse order."\
				.format(self.a, self.b))
		
		else:  # straight order or a == b
			if self.a > self.b:
				raise ValueError("Start value ({0}) can't be larger stop ({1}) while straight order."\
				.format(self.a, self.b))
		
		# we check return type
		if not ((self.return_type == 'dec') or (self.return_type == 'float') or 
				(self.return_type == 'str') or (self.return_type == 'int')):
					raise ValueError("Return type must be one of: 'dec', 'float', 'str', 'int', it was {0}.".format(type(self.return_type)))
	
	
	
	
	def __iter__(self):
		self.first_time = True  # to return a first
		self.current = self.a
		return self
	
	
	def __next__(self):
	
		if self.first_time:  # first value == self.a
			self.first_time = False
			return self.return_depending_type(self.a)
		
		self.current += self.step
		
		if self.a < self.b:  # straight order
			if self.current <= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		elif self.a > self.b:  # reverse order
			if self.current >= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		else:  # a == b
			if self.current == self.a:
				return self.return_depending_type(self.a)
			else:
				raise StopIteration()
	
	
	
	
	def __len__(self):
		try:
			self.length
		except AttributeError:  # if no such attribute
			return int((self.b - self.a) / self.step + 1)
		else:
			return self.length
	
	
	
	
	get = humlist.get  # humlist was created dynamically
	
		
	def __getitem__(self, key):
		'''Returns one value if there's one key (it's int),
		or new appropriate humdrange instance, if key is slice.
		rev. 3
		'''
		if type(key) == int:
		
			self.check_key_for_errors(key)
			key = self.replace_negative_keys(key)
			
			if self.a == self.b:
				return self.return_depending_type(self.a)
			
			else:  # straight or reverse order resolved mathematically
				return self.return_depending_type(self.a + (self.step * (key - 1)))
		
		elif type(key) == slice:
		
			self.check_slice_for_errors(key)
			key = self.replace_negative_keys(key)
			
			backup = self.return_type  # hack. if it'll be float - it'll pass it (float) to new
			self.return_type = 'dec'  # humdrange's .__init__() method - it'll give errors.
			
			if key.step:
				step = key.step * self.step
			else:
				step = self.step
			
			if step > 0:  # straight order
				if self.step > 0:
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.a
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.b
				else: # self.step < 0
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.b
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.a
			
			else:  # step < 0, reverse order
				if self.step > 0: 
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.b
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.a
				else: # self.step < 0
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.a
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.b				
			
			self.return_type = backup  # return back from hack
			
			return humdrange(start, stop, step, self.return_type)
		
		else:
			raise TypeError('Key is not of an appropriate type. It must be int or slice.')
	
	
	
	
	def check_key_for_errors(self, key):
		'''Is used in .__getitem__().
		'''		
		# check in diapason
		if not ((1 <= key <= self.__len__()) or (-1 >= key >= -self.__len__()) ):
			raise IndexError("Key index ({now}) out of range (from 1 to {len} or -1 to -{len}).".format(len=self.__len__(), now=key))
	
	
	
	
	def check_slice_for_errors(self, key):
		'''Is used in .__getitem__().
		'''
		# check types of elements (to be int or None)
		if not ( (type(key.start) == int) or (key.start == None) ):
			raise TypeError("Start value must be int or omitted (now it is {0}).".format(key.start))
		if not ( (type(key.stop) == int) or (key.stop == None) ):
			raise TypeError('Stop value must be int or omitted (now it is {0}).'.format(key.start))
		if not ( (type(key.step) == int) or (key.step == None) ):
			raise TypeError('Step value must be int or omitted (now it is {0}).'.format(key.start))	
		
		
		# check start and stop indexes to be in diapason or None	
		if key.start != 0:
			if key.start:  # None cannot be compared to int
				if not ((1 <= key.start <= self.__len__()) or (-1 >= key.start >= -self.__len__())):
					raise IndexError('Start key index ({ind}) out of range (from 1 to {rng} or -1 to -{rng}).'\
					.format(ind=key.start, rng=self.__len__()))
		else:
			raise IndexError('Slice start value cannot be equal zero.')
		if key.stop != 0:
			if key.stop:  # None cannot be compared to int
				if not ((1 <= key.stop <= self.__len__()) or (-1 >= key.stop >= -self.__len__())):
					raise IndexError('Stop key index ({ind}) out of range (from 1 to {rng} or -1 to -{rng}).'\
					.format(ind=key.stop, rng=self.__len__()))
		else:
			raise IndexError('Slice stop value cannot be equal zero.')
		
		
		# check key.step, check start and stop depending on order (step sets order)
		if key.step != 0:  # because if it's None, than will be error while "key.step > 0"
						
			if (key.step == None) or (key.step > 0):  # straight order
				if key.start:
					start = self.replace_negative_keys(key.start)
				else:
					start = 1
				if key.stop:
					stop = self.replace_negative_keys(key.stop)
				else:
					stop = self.__len__()
					
				if start > stop:
					raise ValueError('Slice start value ({start}) cannot be larger stop ({stop}) while straight order.'\
					.format(start=key.start, stop=key.stop))
			
			else:  # key.step < 0, reverse order
				if key.start:
					start = self.replace_negative_keys(key.start)
				else:
					start = self.__len__()
				if key.stop:
					stop = self.replace_negative_keys(key.stop)
				else:
					stop = 1
				
				if start < stop:
					raise ValueError('Slice start value ({start}) cannot be lesser stop ({stop}) while reverse order.'\
					.format(start=key.start, stop=key.stop))
			
		else:  # key.step == 0
			raise ValueError('Slice step cannot be zero.')	
	
	
	
	
	def replace_negative_keys(self, key):
		'''Replaces negative key's values (which mean counting from the end of range)
		with positive ones (which mean counting from start of range).
		It doesn't return anything - it replaces so it is.
		rev. 2
		'''
		if type(key) == int:
			if key < 0:
				key = (self.__len__() + 1) + key  # "-" on "-" gives "+"
			return key
			
		elif type(key) == slice:
			if key.start and (key.start < 0):
				start = (self.__len__() + 1) + key.start  # + -key will give - key
			else:
				start = key.start
			
			if key.stop and (key.stop < 0):
				stop = (self.__len__() + 1) + key.stop
			else:
				stop = key.stop
		
			return slice(start, stop, key.step)
	
	
	
	
	def return_depending_type(self, value):
		'''Returns value, depending on return type, specified in __init__().
		rev. 1
		'''
		if self.return_type == 'dec':
			return value
		elif self.return_type == 'float':
			return float(value)
		elif self.return_type == 'str':
			return str(value)
		else:  # == 'int'
			return int(value)




class drange(humdrange):
	def __getitem__(self, key):
		key = change_indexes_0_to_1(key)
		#сheck_indexes_0_to_1(key)
		return self.__class__.__base__.__getitem__(self, key)



