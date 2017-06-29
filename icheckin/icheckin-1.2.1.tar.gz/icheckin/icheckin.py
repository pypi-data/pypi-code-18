import requests
import sys
from getpass import getpass
from os.path import exists
from icheckin import constants, commands

def main():
	# Command-line tools
	if len(sys.argv) > 1:
		commands.process(sys.argv[1:])
		sys.exit()

	# Check for updates
	update = _checkUpdate(constants.UPDATES, constants.VERSION)
	if update is not None:
		print(update+'\n')

	# Start a session
	session = requests.Session()

	extracted = True
	while True:
		if exists(constants.PATH):
			# Extract credentials
			credentials = _extractCredentials(constants.PATH, constants.KEYWORD_1, 
				constants.KEYWORD_2)
			if type(credentials) == str:
				print(credentials)
				sys.exit()
		else:
			# Prompt for credentials
			credentials = (input('Student ID: '), getpass('Password: '))
			extracted = False
			if '' in credentials:
				sys.exit()
		# Login to iZone
		payload = {
			'form_action': 'submitted',
			'student_uid': credentials[0],
			'password': credentials[1],
		}
		login = _loginIzone(session, constants.LOGIN, payload)
		if login is None:
			break
		else:
			print(login)
			if extracted:
				sys.exit()
			else:
				print()

	# Save credentials
	if not extracted:
		print('Save your credentials?')
		while True:
			save = input('(Y to save / Enter to ignore) ')
			if save == '':
				break
			if save.upper() == 'Y':
				commands.process(['-s', credentials[0], credentials[1]])
				break
		print()

	while True:	
		# Prompt for code
		code = input('Code: ')
		if code == '':
			sys.exit()
		# Check for SunwayEdu Wi-Fi
		sunway = _checkSunwayWifi(constants.WIFI)
		if sunway is not None:
			print(sunway+'\n')
			continue
		# Check in with code
		checkin = _checkinCode(session, constants.CHECKIN, code)
		if checkin is None:
			print('Successfully checked in.')
			break
		else:
			print(checkin+'\n')

def _checkUpdate(u, v):
	''' 
	-> None	: Version is latest or checking failed
	-> str 	: Update message for when a newer version is available 
	'''
	try:
		r = requests.get(u, timeout=2)
	except (requests.ConnectionError, requests.ConnectTimeout, 
		requests.ReadTimeout):
		return None
	else:
		latestVersion = r.json()['latest_version']
		if v != latestVersion:
			return 'A newer version (%s) is available.\n' % latestVersion +\
				'$ pip install --upgrade icheckin'
		else:
			return None

def _extractCredentials(p, k1, k2):
	''' 
	-> tuple	: Student ID and password 
	-> str 	: Error message
	'''
	with open(p, 'r') as file:
		lines = list(map(str.strip, file.readlines()))
		# Check format of file content
		if len(lines) == 5 and lines[0] == k1 and lines[3] == k2:
			return (lines[1], lines[4])
		else:
			return 'error: something is wrong with %s\n\
				Save your credentials again or remove your credentials.' % p

def _loginIzone(s, lg, pl):
	''' 
	-> None	: Login successful
	-> str 	: Error message 
	'''
	try:
		r = s.post(lg, data=pl)
	except requests.ConnectionError:
		return 'No internet connection.'
	if r.history:
		return None
	else:
		return 'Invalid credentials.'

def _checkSunwayWifi(w):
	''' 
	-> None	: Connected to SunwayEdu Wi-Fi
	-> str 	: Error message
	'''
	try:
		r = requests.get(w, timeout=2)
	except requests.ConnectTimeout:
		return 'Not connected to SunwayEdu Wi-Fi.'
	except requests.ConnectionError:
		return 'No internet connection.'
	else:
		return None

def _checkinCode(s, ci, co):
	try:
		r = s.post(ci, data={'checkin_code': co}, timeout=2)
	except (requests.ReadTimeout, requests.ConnectionError):
		return 'No internet connection.'
	if 'Checkin code not valid.' in r.text or\
		'The specified URL cannot be found.' in r.text:
		return 'Invalid code.'
	else:
		return None

if __name__ == '__main__':
	main()