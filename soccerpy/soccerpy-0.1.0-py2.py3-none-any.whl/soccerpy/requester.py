import requests
from soccerpy.exceptions import *
from soccerpy.endpoint_manager import EndpointManager


class Requester(EndpointManager):
    def __init__(self, API_KEY="", response_format="full"):
        super().__init__()
        self.API_KEY = API_KEY
        self.response_format = response_format
        self.headers = {'X-Auth-Token': self.API_KEY,
                        'X-Response-Control': self.response_format}
        self.r = object

    def request(self, endpoint_name=None, endpoint_format=False, payload=None, raw=False, raw_url=None):
        if payload is None:
            payload = {}
        if endpoint_format:
            raw_url = self.endpoints[endpoint_name]
            url = raw_url.format(endpoint_format)
        elif raw_url:
            url = raw_url
        else:
            url = self.endpoints[endpoint_name]
        self.r = requests.get(url, headers=self.headers, params=payload)
        data = self.check_for_exceptions(self.r)
        if raw:
            return self.r
        return data, self.r.headers

    @staticmethod
    def check_for_exceptions(request):
        data = request.json()
        if "error" in data:
            print(data['error'])
        status_code = request.status_code
        if status_code == 400:
            raise BadRequestException("Your request was malformed most likely the value"
                                      " of a Filter was not set according to the Data Type"
                                      " that is expected.")
        elif status_code == 403:
            raise RestrictedResourceException("You tried to access a resource that exists,"
                                              " but is not available for you.This can be out of"
                                              " the following reasons here at:"
                                              "https://api.football-data.org/docs/latest/"
                                              "index.html#_errors")
        elif status_code == 404:
            raise NotFoundException("You tried to access a resource that doesn’t exist.")
        elif status_code == 429:
            raise TooManyRequestsException("You exceeded your allowed requests per minute/day"
                                           " depending on API version and your user status. "
                                           "Look at Request-Throttling for more information.")
        elif "error" in data:
            raise GeneralException(data['error'])
        else:
            return data
