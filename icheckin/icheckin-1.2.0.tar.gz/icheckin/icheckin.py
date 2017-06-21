import requests
import getpass
import sys
import os
from os.path import join, expanduser, exists

VERSION = '1.2.0'

UPDATES = 'http://chunkhang.pythonanywhere.com/icheckin/api'
LOGIN = 'https://izone.sunway.edu.my/login'
WIFI = 'https://icheckin.sunway.edu.my/otp/CheckIn/isAlive/CuNv9UV2rXg4WtAsXUPNptg6gWQTZ52w'
CHECKIN = 'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'
KEYWORD_1 = '[Student ID]'
KEYWORD_2 = '[Password]'
PATH = join(expanduser("~"), '.icheckin-credentials')
USAGE = 'usage: icheckin [-h | --help] [-c | --credentials <student id> <password>]\n\t\t[-r | --remove]'
CREDENTIALS = 'Re-enter credentials like so:\nicheckin -c <student id> <password>\nOr remove the saved credentials like so:\nicheckin -r'

def saveCrendentials(sid, pwd):

	with open(PATH, 'w') as file:
		file.write(KEYWORD_1+'\n')
		file.write(sid+'\n\n')
		file.write(KEYWORD_2+'\n')
		file.write(pwd+'\n')
	print('success: credentials saved to %s' % PATH)

def main():

	# Process command-line arguments
	length = len(sys.argv)
	if length > 1:
		command = sys.argv[1]
		if command == '-h' or command == '--help':
			# Help
			print(USAGE + '\n')
			print('   -c, --credentials\tSave credentials to skip the login process')
			print('   -r, --remove\t\tRemove saved credentials')
			print('   -h, --help\t\tDisplay help')
		elif command == '-c' or command == '--credentials':
			# Save credentials
			if length == 4:
				saveCrendentials(sys.argv[2], sys.argv[3])
			else:
				print('error: invalid number of arguments')
				print('Provide crendentials like so:')
				print('icheckin -c <student id> <password>')
		elif command == '-r' or command == '--remove':
			# Remove credentials
			if exists(PATH):
				os.remove(PATH)
				print('success: crendentials removed')
			else:
				print('error: no saved credentials to remove')
		else:
			print('unknown command: %s' % command)
			print(USAGE)
		sys.exit(0)

	# Check for updates
	try:
		r = requests.get(UPDATES, timeout=2)
	except (requests.ConnectionError, requests.ConnectTimeout):
		# Skip checking
		pass
	else:
		latestVersion = r.json()['latest_version']
		if VERSION != latestVersion:
			print('A newer version (%s) is available.' % latestVersion)
			print('$ pip install --upgrade icheckin\n')

	# Start a session
	s = requests.Session()

	# Login to iZone
	while True:
		studentID = ''
		password = ''
		saved = False 
		if exists(PATH):
			# Extract credentials
			with open(PATH, 'r') as file:
				lines = list(map(str.strip, file.readlines()))
				if len(lines) == 5 and lines[0] == KEYWORD_1 and lines[3] == KEYWORD_2:
					studentID = lines[1]
					password = lines[4]
					saved = True
				else:
					print('error: something is wrong with %s' % PATH)
					print(CREDENTIALS)
					sys.exit(1)
		else:
			studentID = input('Student ID: ')	
			if studentID == '':
				sys.exit(0)
			password = getpass.getpass('Password: ')
			if password == '':
				sys.exit(0)
		payload = {
			'form_action': 'submitted',
			'student_uid': studentID,
			'password': password,
		}
		try:
			r = s.post(LOGIN, data=payload)
		except requests.ConnectionError:
			print('No internet connection.')
			if saved:
				sys.exit(1)
			else:
				print()
				continue
		if r.history:
			break
		else:
			print('Invalid credentials.')
			if saved:
				print(CREDENTIALS)
				sys.exit(1)
			else:
				print()

	# Prompt to save credentials
	if not saved:
			print('Do you want to save your credentials?')
			while True:
				answer = input('(Y to save / Enter to ignore) ')
				if answer == '':
					break
				if answer.upper() == 'Y':
					# Save credentials
					saveCrendentials(studentID, password)
					break

	# Submit check-in code
	firstTime = True
	while True:
		if not saved:
			print()
		else:
			if not firstTime:
				print()
			else:
				firstTime = False
		code = input('Code: ')
		if code == '':
			sys.exit(0)
		# Check for SunwayEdu Wi-Fi
		try:
			r = requests.get(WIFI, timeout=2)
		except requests.ConnectTimeout:
			print('Not connected to SunwayEdu Wi-Fi.')
			continue
		except requests.ConnectionError:
			print('No internet connection.')
			continue
		try:
			r = s.post(CHECKIN, data={'checkin_code': code}, timeout=2)
		except (requests.ReadTimeout, requests.ConnectionError):
			print('No internet connection.')
			continue
		if 'Checkin code not valid.' in r.text or 'The specified URL cannot be found.' in r.text:
			print('Invalid code.')
		else:
			print('Successfully checked in.')
			break

if __name__ == '__main__':
	main()
