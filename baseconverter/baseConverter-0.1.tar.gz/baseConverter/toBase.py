def toBaseTen(n, base):
	'''
	This function takes arguments: number that you want to convert and its base
	It will return an int in base 10
	Examples:
	..................
	>>> toBaseTen(2112, 3)
	68
	..................
	>>> toBaseTen('AB12', 12)
	61904
	..................
	>>> toBaseTen('AB12', 16)
	111828
	..................
	'''
	baseTen = 0
	num = str(num)
	for i in range(len(num)):
		baseTen += base ** (len(num) - 1 - i)  * int(num[i], 36)
	return baseTen

def toAnyBase(num, base):
	'''
	This function takes 2 arguments: number (in base 10, if you have number in any other base, 
	please use toBaseTen function first to get get your number in base 10) and base that you
	want to convert your number to.
	It will return a string
	Examples:
	..................
	>>> toAnyBase(23412,30)
	'Q0C'
	..................
	>>>	toAnyBase(23412,15)
	'6E0C'
	..................
	>>> toAnyBase(12, 2)
	'1100'

	'''
	bases = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	if num < base:
		return bases[num]
	else:
		return toAnyBase(num // base, base) + bases[num % base]