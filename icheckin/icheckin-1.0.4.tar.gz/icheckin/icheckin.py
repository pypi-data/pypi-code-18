import requests
import getpass
import sys

def main():

	LOGIN = r'https://izone.sunway.edu.my/login'
	CHECKIN = r'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'

	argumentsPassed = False
	if len(sys.argv) > 1:
		if len(sys.argv) == 3:
			studentID = sys.argv[1]
			password = sys.argv[2]
			argumentsPassed = True
		else:
			print('Usage: icheckin <student id> <password>')
			sys.exit(1)

	s = requests.Session()

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
			print('Connection problem.')
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
		try:
			r = s.post(CHECKIN, data={'checkin_code': code}, timeout=2)
		except (requests.ReadTimeout, requests.ConnectionError):
			print('Connection problem.')
			continue
		if 'Checkin code not valid.' in r.text:
			print('Invalid code.')
		else:
			print('Successfully checked in.')
			break

if __name__ == '__main__':
	main()
