import requests
from .utils import raise_for_error, get_timestamp

class EthOSAPI(object):

    _error      = None
    custompanel = None
    endpoint    = "http://%s.ethosdistro.com/"

    def __init__(self, custompanel=None):

        if custompanel is None:
            raise Exception("custompanel is not defined. Please have look to http://########.ethosdistro.com")
        else:
            self.endpoint    = self.endpoint % custompanel
            self.custompanel = custompanel

    @property
    def last_error(self):
        return self._error

    def make_request(self, method, path, data=None, params=None, headers=None, timeout=60):
        if headers is None:
            headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
        else:
            headers.update({'x-li-format': 'json', 'Content-Type': 'application/json'})

        if params is None:
            params = {}
        kw = dict(data=data, params=params, headers=headers, timeout=timeout)

        url = self.endpoint + path

        return requests.request(method.upper(), url, **kw)

class EthOSApplication(EthOSAPI):

    def get_summary(self):
        params = dict()
        params.update({'json': 'yes'})

        response = self.make_request('GET', "", params=params)
        raise_for_error(response)

        payload = dict()

        payload["success"] = True
        payload ["timestamp"] = get_timestamp()

        if response.text != "":
            payload["payload"] = response.json()
        else:
            payload["payload"] = dict()

        return payload
