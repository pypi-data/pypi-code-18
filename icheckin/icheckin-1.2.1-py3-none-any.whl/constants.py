from os.path import join, expanduser, realpath, dirname

# Version
VERSION = '1.2.1'

# URLs
UPDATES = 'http://chunkhang.pythonanywhere.com/icheckin/api'
LOGIN = 'https://izone.sunway.edu.my/login'
WIFI = 'https://icheckin.sunway.edu.my/otp/CheckIn/isAlive/' +\
	'CuNv9UV2rXg4WtAsXUPNptg6gWQTZ52w'
CHECKIN = 'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'

# Credentials
KEYWORD_1 = '[Student ID]'
KEYWORD_2 = '[Password]'
PATH = join(expanduser("~"), '.icheckin-credentials')
TEST_PATH = join(dirname(dirname(realpath(__file__))), 'test/.test-credentials')