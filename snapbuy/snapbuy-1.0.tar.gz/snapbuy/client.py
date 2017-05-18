import requests


class HttpClient(object):
    def __init__(self, api_key, api_url):
        self.api_url = api_url
        self.headers = {'x-api-key': api_key}

    def do_get(self, path, params=None, deserializer=None):
        try:
            res = requests.get(self.api_url + path, headers=self.headers, params=params)
            json = res.json()

            return deserializer(json) if deserializer is not None else json
        except Exception as ex:
            return {'statusText': "Fatal error", 'errorMessage': str(ex)}

    def do_post(self, path, data=None, files=None, deserializer=None):
        try:
            res = requests.post(self.api_url + path, headers=self.headers, data=data, files=files)
            json = res.json()

            return deserializer(json) if deserializer is not None else json
        except Exception as ex:
            return {'statusText': "Fatal error", 'errorMessage': str(ex)}

    def do_delete(self, path, data=None, deserializer=None):
        try:
            res = requests.delete(self.api_url + path, headers=self.headers, data=data)
            json = res.json()

            return deserializer(json) if deserializer is not None else json
        except Exception as ex:
            return {'statusText': "Fatal error", 'errorMessage': str(ex)}
