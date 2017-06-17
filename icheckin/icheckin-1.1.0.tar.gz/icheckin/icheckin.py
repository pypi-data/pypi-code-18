import requests
import getpass
import sys

def main():

	VERSION = '1.1.0'
	UPDATES = r'https://pypi.python.org/pypi/icheckin'
	LOGIN = r'https://izone.sunway.edu.my/login'
	WIFI = r'https://icheckin.sunway.edu.my/otp/CheckIn/isAlive/CuNv9UV2rXg4WtAsXUPNptg6gWQTZ52w'
	CHECKIN = r'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'

	# Process command-line arguments
	argumentsPassed = False
	if len(sys.argv) > 1:
		if len(sys.argv) == 3:
			studentID = sys.argv[1]
			password = sys.argv[2]
			argumentsPassed = True
		else:
			print('Usage: icheckin <student id> <password>')
			sys.exit(1)

	# Check for updates
	try:
		r = requests.get(UPDATES)
	except requests.ConnectionError:
		# Skip checking
		pass
	else:
		if 'icheckin '+VERSION not in r.text:
			print('A newer version of icheckin available.\n(pip install --upgrade icheckin)\n')

	# Start a session
	s = requests.Session()

	# Login to iZone
	while True:
		if not argumentsPassed:
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
			if argumentsPassed:
				sys.exit(1)
			else:
				print()
				continue
		if r.history:
			break
		else:
			print('Invalid credentials.')
			if argumentsPassed:
				sys.exit(1)
			else:
				print()

	# Submit check-in code
	firstTime = True
	while True:
		if not argumentsPassed:
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
