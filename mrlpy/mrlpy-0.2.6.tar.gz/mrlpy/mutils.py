import string
import random
'''
Utility methods and variables
'''


AUTO_GEN_NAMES=False

def genID(size=6, chars=string.ascii_uppercase + string.digits):
	'''
	Generate a random ID for creating unique names
	'''
	return ''.join(random.choice(chars) for _ in range(size))
