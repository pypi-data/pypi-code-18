from rest_client.lib.client import Client
from rest_client.lib.fields import Field

from rest_client.lib.exceptions import EndpointError


class Endpoint(object):
    """
    This is the main class for all Endpoints. 
    To use it you have to put that class as parent in your Endpoint Class.
    
    Mandatory objects what you have to set in your Endpoints are:
        * endpoint - the path to your endpoint i.e. `/user/{user_id}/details/`.
                     To use endpoint parameters put them like that: {endpoint_parameter} in your endpoint's path.
        * method   - GET, POST, PUT, PATCH or DELETE method. You can set it as Request.GET or as a string 'get'.
        
    Optional objects:
        All of those objects you should set as Endpoint's fields:
            * header (dict)  - set it if you need to send request to endpoints with some headers values.
            * cookies (dict) - set it when you need include cookies inside your request.
            * auth (tuple)   - set it when you need authorization in your requests. This field should be set as 
                               instance of auth class. Check auth.py file.
            * payload (dict) - set it when you need to send GET or POST or PATCH or PUT or DELETE with parameters.
                               You can set it directly as field in Endpoint class or as argument when you create 
                               Endpoint's instance.
                               
        Instance fields:
            * payload (dict)
            * url_params (dict) - you set this when you use parameters in your endpoint path.
    
    How to send request:
        - To send request you have to create your own endpoint's instance.
          params = {'param1': 1, 'param2': 2}
          instance = TestInstagramEndpointGET(url_params=params). Values of keys `param1` and `param2` are set to your 
          endpoint path - `/some/endpoint/{param1}/something/{param2/`.
    """
    endpoint = None
    method = None
    headers = None
    cookies = None
    auth = None
    payload = None

    objects = None

    mandatory_fields = ['endpoint', 'method']

    def __new__(cls, *args, **kwargs):
        """
        Before create instance - checks if all mandatory fields are set in parent class.
        """
        cls.validate()
        return super().__new__(cls)

    def __init__(self, url_params=None, payload=None):
        if url_params:
            self.endpoint = self.endpoint.format(**url_params)

        self.payload = payload or self.payload
        self.request = {
            'endpoint': self.endpoint,
            'method': self.method,
            'headers': self.headers,
            'cookies': self.cookies,
            'auth': self.auth,
            'payload': self.payload
        }
        self.response = Client(self.request).response  # sends request to endpoint and return response.

        # set objects
        self.objects = Field(endpoint_name=self.endpoint_name, values=self.response)

    @property
    def endpoint_name(self):
        return self.__class__.__name__

    @classmethod
    def validate(cls):
        """
        Checks if all mandatory fields are filled.
        """
        for field in cls.mandatory_fields:
            if not getattr(cls, field):
                error_msg = "{field} is mandatory field.".format(field=field)
                raise EndpointError(error_msg)

