
import requests
import base64
import json
is_production = False

if not is_production:
	MASTER_URL = 'https://test.api.promisepay.com/'
else:
	MASTER_URL = 'https://test.api.promisepay.com/'

try:

	from django.conf import settings

	password = settings.PROMISE_PAY_SECRET
	username = settings.PROMISE_PAY_KEY


	AUTH = 'Basic '+base64.b64encode(settings.PROMISE_PAY_KEY+':'+settings.PROMISE_PAY_SECRET)
	HEADERS = {'Authorization': AUTH,"Content-Type": "application/json"}

except:

	username = 'YOUR PROMISEPAY USERNAME'
	password = 'YOUR PROMISEPAY SECRECT'


class PromisePay(object):
	
	def __init__(self):

		if not password and not username:
			AUTH = 'Basic '+base64.b64encode(key+':'+secret)
			HEADERS = {'Authorization': AUTH,"Content-Type": "application/json"}


		self.AUTH = AUTH
		self.HEADERS = HEADERS
		
		

	def get_list(self,path,limit=10,offset=0):

		self.limit = limit
		self.path=path
		self.offset=offset

		payload = {'limit': self.limit, 'offset': self.offset}

		r = requests.get(MASTER_URL+self.path, headers=self.HEADERS,params=payload)
		
		if r.json().has_key('meta'):
			return r.json()
		
		else:
			try:
				
				if r.status_code == 503:
					return {'errors':'Service is down'}
				else:
					return r.json()
			except:
				raise Exception(r.json())


	def get_one(self,path,id=None):
		

		if id:
			r = requests.get(MASTER_URL+path+'/'+id, headers=self.HEADERS)

		else:
			r = requests.get(MASTER_URL+path+'/', headers=self.HEADERS)
		
		if r.status_code == 503:
			return {'errors':'Service is down'}
		
		else:
			print r.json()
			return r.json()



	def delete_one(self,path,id=None):
		
		
		if id:
			r = requests.delete(MASTER_URL+path+'/'+id, headers=self.HEADERS)

		else:
			r = requests.delete(MASTER_URL+path+'/', headers=self.HEADERS)
		

		print "SCODE",r.status_code

		if r.status_code == 200:
			return r.json()

	
		if r.status_code == 503:
			return {'errors':'Service is down'}
		
		else:
			return {'errors':'Something went wrong with service provider'}
		



	def add_one(self,path,data=None):
	
		r = requests.post(MASTER_URL+path, headers=self.HEADERS,data=json.dumps(data))


		if r.status_code == 201:
			return r.json()

		elif r.status_code ==  401:
			raise Exception('Authorization error')


		if r.status_code == 503:
			return {'errors':'Service is down'}
		else:
			return r.json()


	def edit_one(self,path,id,data):

		r = requests.patch(MASTER_URL+path+'/'+id, data=json.dumps(data),headers=self.HEADERS)

		return r
