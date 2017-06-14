import requests
import getpass
import sys

def printUsage():

	print('\nYou can pass your student ID and password as')
	print('command-line arguments to skip the login process.')
	print('Usage: python3 icheckin.py [studentID] [password]')

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
			printUsage()
			sys.exit(1)

	s = requests.Session()
	if not argumentsPassed:
		printUsage()

	while True:
		if not argumentsPassed:
			studentID = input('\nSTUDENT ID: ')
			if studentID == '':
				sys.exit(0)
			password = getpass.getpass('PASSWORD: ')
			if password == '':
				sys.exit(0)
		payload = {
			'form_action': 'submitted',
			'student_uid': studentID,
			'password': password,
		}
		r = s.post(LOGIN, data=payload)
		if r.history:
			break
		else:
			print('\nInvalid credentials.')
			if argumentsPassed:
				sys.exit(1)

	while True:
		code = input('\nCODE: ')
		if code == '':
			sys.exit(0)
		r = s.post(CHECKIN, data={'checkin_code': code})
		if 'Checkin code not valid.' in r.text:
			print('Invalid code.')
		else:
			print('Successfully checked in.')
			break

if __name__ == '__main__':
	main()
