#! /usr/bin/python3
"""Contains functions to change indexes.
"""


def change_indexes_0_to_1(key):
	'''('RU') Функция используется в drange в __getitem__().
	a[1] > a[0]
	Она смещает в последовательностях номер первого элемента с [0] на [1] чтобы показать вам.
	если при a[arg] передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)
	rev. 5
	'''
	if type(key) == int:	
		
		if key >= 0:
			key += 1
	
	elif type(key) == slice:
	
		if key.step and (key.step < 0): # reverse order  
			if key.start and (key.start >= 0):
				start = key.start + 1
			else:
				start = key.start
			
			if key.stop != None:
			
				if key.stop >= 0:
					stop = key.stop + 2
				else:
					stop = key.stop
			else:
				stop = None
			
			key = slice(start, stop, key.step)
	
		else:  # straight order, key.step > 0 and None
			if key.start >= 0:
				start = key.start + 1
			
			key = slice(start, key.stop, key.step)		
	
	return key




def change_indexes_1_to_0(key):
	'''('RU') Функция используется в: __getitem__, __setitem__, __delitem__.
	a[1] > a[0]
	Она смещает в последовательностях номер первого элемента с [1] на [0] когда вы его вводите.
	если в функц. передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)	
	rev. 6
	'''
	if type(key) == int:
		
		if key > 0:
			key -= 1
	
	elif type(key) == slice:
		
		if key.step and (key.step < 0):  # reverse order
			if key.start and (key.start > 0):
				start = key.start - 1
			else:  # key.start == None, or == 0, or < 0.
				start = key.start
			
			if key.stop != None:
				if key.stop >= 2:
					stop = key.stop - 2
				elif 0 <= key.stop  <= 1:
					stop = None
			else:
				stop = key.stop
			
			key = slice(start, stop, key.step)
		
		else:  #  straight order  # key.step > 0 and None
			if key.start and (key.start > 0):
				start = key.start - 1			
				key = slice(key.start - 1, key.stop, key.step)
	
	return key
