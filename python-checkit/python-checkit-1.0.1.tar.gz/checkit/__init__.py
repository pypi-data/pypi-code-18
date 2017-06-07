import requests
import json
import logging


CHECKIT_URL = "https://checkit.metadonors.it/api/v1"

class Checkit(object):
    """An entry point for all requests"""
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', CHECKIT_URL)
        self.token = kwargs.get('apikey', '')
        if not self.token:
            raise Exception("You must provide a valid Checkit APIKEY")

    def iban(self, iban):
        return self.request('post', '/pro/iban/', data={'iban': iban})

    def codicefiscale(self, **kwargs):
        if 'first_name' not in kwargs.keys() or not kwargs['first_name']:
            raise Exception("You must provide a 'first_name' argument")
        if 'last_name' not in kwargs.keys() or not kwargs['last_name']:
            raise Exception("You must provide a 'last_name' argument")
            
        data = {}
        data['first_name'] = kwargs.get('first_name')
        data['last_name'] = kwargs.get('last_name')
        data['code'] = kwargs.get('code', '')
        data['dob'] = kwargs.get('dob', None)
        data['pob'] = kwargs.get('pob', '')
        data['sex'] = kwargs.get('sex', '')
        print(data)

        return self.request('post', '/pro/it/ssn/', data=data)
        
    def creditcard(self, number):
        if not number.isdigit():
            raise Exception("Credit Card number not valid")
        return self.request('post', '/creditcard/', data={'creditcard': number})

    def email(self, email):
        return self.request('post', '/email/', data={'address': email})
    
    def request(self, method, path, headers=None, params=None, data=None, raw_response=False):
        url = "{}{}".format(self.url, path)         
        kwargs = dict(**{
            'headers': headers or {},
            'params': params or {},
            'data': data or {},
        })

        if method in ('post', 'put'):
            kwargs['data'] = json.dumps(data)
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['headers']['Authorization'] = 'Token %s' % self.token

        response = getattr(requests, method)(url, **kwargs)

        print(kwargs)
        if response.status_code in (200, 201):
            try:
                return response.json()
            except Exception as e:
                print(e)
                raise JSONDecodeError(response)

        if response.status_code == 400:
            raise Exception("Bad request")

        if response.status_code == 401:
            raise Exception("Not Authorized")

        if response.status_code == 403:
            raise Exception("Forbidden")
