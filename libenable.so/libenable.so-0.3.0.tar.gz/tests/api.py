from requests import get, post
import unittest

class ApiTest(unittest.TestCase):
	'''
	Tests the RESTful API to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Verifies that the application is running
		'''

		try:
			get('http://localhost')
		except:
			self.fail(
				'Could not connect, the application is not running on port 80'
			)

	def test_version(self):
		'''
		Tests that the API handles the version route correctly
		'''

		data = get('http://localhost/api/version').json()
		self.assertTrue('version' in data)

	def test_statistics(self):
		'''
		Tests that the API handles the statistics route correctly
		'''

		data = get('http://localhost/api/statistics').json()
		self.assertTrue('libenable' in data)
		self.assertTrue('status' in data['libenable'])
		self.assertTrue('running_tasks' in data['libenable'])
		self.assertTrue('total_tasks' in data['libenable'])
		self.assertTrue('status_code' in data['libenable'])
		self.assertTrue('version' in data['libenable'])
		self.assertTrue('python' in data)
		self.assertTrue('platform' in data['python'])
		self.assertTrue('version' in data['python'])
		self.assertTrue('time' in data)
		self.assertTrue('current' in data['time'])
		self.assertTrue('running' in data['time'])
		self.assertTrue('start' in data['time'])

	def test_reCAPTCHA(self):
		'''
		Tests that the API handles the reCAPTCHA route correctly
		'''

		data = {'site_key': '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'}
		data = post('http://localhost/api/reCAPTCHA', data = data).json()
		self.assertTrue('result' in data)
		self.assertTrue(data['result'])

	def test_solve_media(self):
		'''
		Tests that the API handles the Solve Media route correctly
		'''

		data = {'site_key': 'mlFwzmfg.OLZWwwByqjR6pe.wiwACDEY'}
		data = post('http://localhost/api/solvemedia', data = data).json()
		self.assertTrue('result' in data)
		self.assertTrue('response' in data['result'])
		self.assertTrue('challenge' in data['result'])
		self.assertTrue(data['result'])
		self.assertTrue(data['result']['response'])
		self.assertTrue(data['result']['challenge'])
