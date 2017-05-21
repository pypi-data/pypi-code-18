"""
Convert string to decima, hexa,  binary, octan and reverse
"""
class ConvertExecption(Exception):
	def __init__(self, error):
		print error

def b2s(bstring):
	"""
		bstring: binary string
		return: ascii string
	"""
	if (len(bstring) % 8):
		raise ConvertExecption("String length binary not divisible 8")
	string = ""
	lbin = [bstring[i: i+8] for i in xrange(0,len(bstring), 8)]
	for char in lbin:
		return ''.join(map(lambda x:chr(int(x,2)), lbin))

def s2b(sstring):
	a = lambda x: bin(ord(x))[2:]
	b = lambda y: "0" * (8 - len(y)) + y
	return ''.join(map(lambda x:b(a(x)), sstring))


def s2h(sstring):
	return sstring.encode('hex')

def h2s(hstring):
	return hstring.decode('hex')


def s2d(sstring):
	return int(s2h(sstring), 16)


def d2s(dstring):
	return hex(int(dstring))[2:].decode('hex')