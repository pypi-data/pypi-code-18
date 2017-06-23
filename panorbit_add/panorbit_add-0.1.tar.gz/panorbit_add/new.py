import pyotp

def generateotp():
	totp = pyotp.TOTP('base32secret3232')
	return totp.now() # => 492039