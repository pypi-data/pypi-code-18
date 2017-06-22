import pyotp
totp = pyotp.TOTP('base32secret3232')


def hello():
	return "hello world"

def add(a,b):
	return a+b

def mul(a,b):
	return a-b


def generate_otp():
	return totp.now()