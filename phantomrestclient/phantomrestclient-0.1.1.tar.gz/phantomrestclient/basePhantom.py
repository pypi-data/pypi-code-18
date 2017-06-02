import os
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


class _BasePhantom:
    """
    Base class for the other Phantom instances for holding common/reusable logic and
    for setting up the base connection information to the Phantom instance
    """
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def __make_rest_request__(self, url, method, data=None):
        """
        This is the main method for making the actual REST call to the Phantom endpoints.
        parameters:
            url - The full url endpoint to make the request to
            method - the HTTP method to use for the request (GET, POST)
            data - the data to POST to the url endpoint
        """
        if method.lower() == "post":
            response = requests.post(url, data=json.dumps(data), auth=(self.username, self.password), verify=False)
        elif method.lower() == "get":
            response = requests.get(url, auth=(self.username, self.password), verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            return response

    def get_build_action(self):
        url = os.path.join(self.host, "build_action")
        return self.__make_rest_request__(url, "GET")
