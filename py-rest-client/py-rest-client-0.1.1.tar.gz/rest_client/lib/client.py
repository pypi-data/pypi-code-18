import urllib.parse

import importlib
import os
import requests
from rest_client.lib.exceptions import ClientError
from rest_client.lib.utils.decorators import response_validation

settings = importlib.import_module(os.environ.get('REST_CLIENT_SETTINGS_MODULE'))


class Client(object):
    """
    Main class where we send requests to endpoints and returns responses.
    """
    request = None
    response = None
    endpoint = None

    protocol = settings.REST_SERVER_PROTOCOL
    host = settings.REST_SERVER_HOST
    port = settings.REST_SERVER_PORT

    mandatory_fields = ['protocol', 'host', 'port']

    def __new__(cls, *args, **kwargs):
        """
        Before create instance - checks if all mandatory fields are set in parent class.
        """
        cls.validate()
        return super().__new__(cls)

    def __init__(self, request):
        self.endpoint = request['endpoint']
        self.send_request(request)

    @classmethod
    def validate(cls):
        """
        Checks if all mandatory fields are set.
        """
        for field in cls.mandatory_fields:
            if not getattr(cls, field):
                error_msg = "{field} is mandatory field.".format(field=field)
                raise ClientError(error_msg)

    def get_url(self):
        """
        Builds endpoint absolute url from protocol, host and port variables.
        """
        server_url = "{protocol}://{host}:{port}".format(
            protocol=self.protocol,
            host=self.host,
            port=self.port
        )
        url = urllib.parse.urljoin(server_url, self.endpoint)
        return url

    def send_request(self, request):
        """
        Sends request to endpoint absolute url.
        """
        request['endpoint'] = self.get_url()
        request = Request(**request)

        self.response = request.send()


class Response(object):
    """
    This class handles endpoint's response.
    """
    status = None
    results = None
    errors = None
    content = None

    def __init__(self, request):
        self.content = self.get_content(request)
        self.reason = request.reason
        self.status_code = request.status_code

    @response_validation
    def get_content(self, request):
        """
        Returns content data.
        """
        return request.json()


class Request(object):
    """
    This class handles endpoint's request.
    """
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'

    METHODS = (
        (GET, 'get'),
        (POST, 'post'),
        (PUT, 'put'),
        (PATCH, 'patch'),
        (DELETE, 'delete'),
    )

    def __init__(self, endpoint, method, headers=None, cookies=None, auth=None, payload=None):
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.auth = auth
        self.endpoint = endpoint

        self.payload = payload

    def is_method_get(self):
        """
        Checks if current method is a GET method.
        """
        return self.method == self.GET

    def set_payload(self, params):
        """
        Set payload value as correct key.
        For method GET we need to set it as `params`. For other methods it is `data`.
        """
        if self.is_method_get():
            params['params'] = self.payload

        else:
            params['data'] = self.payload

        return params

    def handle_request(self, params):
        """
        Send correct request with filled params.
        """
        request = requests

        if self.cookies:
            request = request.Session()

        return getattr(request, self.method)(**params)

    def send(self):
        """
        Sends request to endpoint's absolute url. 
        For more info go to: http://docs.python-requests.org
        """
        params = {
            'url': self.endpoint,
            'headers': self.headers,
            'cookies': self.cookies,
            'auth': self.auth,
        }

        params = self.set_payload(params)
        request = self.handle_request(params)

        response = Response(request)

        return response.content
