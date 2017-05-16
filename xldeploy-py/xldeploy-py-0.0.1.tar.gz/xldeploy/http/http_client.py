import requests
import json
from xldeploy.errors import XLDeployException, XLDeployConnectionError, XLDeployConnectionTimeout, create_api_error_from_http_exception


class HttpClient:

    __headers = {'content-type': 'application/json', 'Accept': 'application/json', 'Accept-Type': 'application/json'}

    def __init__(self, config):
        self.config = config

    def get_url(self, path=""):
        return "%s://%s:%s/%s%s" % (self.config.protocol, self.config.host, self.config.port, self.config.context_path, path)

    def get_credentials(self):
        return (self.config.username, self.config.password)

    def authenticate(self):
        print "Connecting to the XL Deploy server at %s..." % (self.get_url())
        response = requests.get(self.get_url() + "/server/info",
                                auth=self.get_credentials())
        if response.status_code == 200:
            print "Successfully connected."
        elif response.status_code == 401 or response.status_code == 403:
            raise ValueError("You were not authenticated correctly, did you use the correct credentials?")
        elif response.status_code == 402:
            raise ValueError(
                "License not found, invalid, or expired; see the XL Deploy logs. Please contact your XebiaLabs sales representative for a valid license")
        else:
            raise ValueError("Could contact the server at %s but received an HTTP error code %s" % (
            self.get_url(), response.status_code))

    def get(self, path, headers=__headers, params={}):
        json_data = None
        try:
            response = requests.get(self.get_url(path), params=params, auth=self.get_credentials(), headers=headers)
            response.raise_for_status()
            if response.status_code == 204:
                return
            if 199 < response.status_code < 399:
                json_data = json.loads(response.text)
        except Exception as e:
            try:
                json_data = json.loads(response.text)
            except:
                raise self.raise_xld_exception(e)

        return json_data

    def delete(self, path, headers=__headers, params={}):
        try:
            response = requests.delete(self.get_url(path), params=params, auth=self.get_credentials(), headers=headers)
        except Exception as e:
            try:
                json_data = json.loads(response.text)
            except:
                raise self.raise_xld_exception(e)

        return response


    def post(self, path, headers=__headers, params={}, body=None):
        json_data = None
        try:
            if body != None:
                body = json.dumps(body)
            response = requests.post(self.get_url(path), params=params, auth=self.get_credentials(), headers=headers, data=body)
            json_data = None
            response.raise_for_status()
            if response.status_code == 204:
                return
            elif 199 < response.status_code < 399:
                json_data = json.loads(response.text)
        except Exception as e:
            try:
                json_data = json.loads(response.text)
            except:
                raise self.raise_xld_exception(e)

        return json_data

    def put(self, path, headers=__headers, params={}, body=None):
        try:
            if body != None:
                body = json.dumps(body)
            response = requests.put(self.get_url(path), params=params, auth=self.get_credentials(), headers=headers, data=body)
            response.raise_for_status()
            if response.status_code == 204:
                return
            if 199 < response.status_code < 399:
                json_data = json.loads(response.text)
        except Exception as e:
            try:
                json_data = json.loads(response.text)
            except:
                raise self.raise_xld_exception(e)

        return json_data

    def raise_xld_exception(self, e):
        if isinstance(e, requests.exceptions.Timeout):
            raise XLDeployConnectionTimeout('Timeout connecting to {0}'.format(self.config.host))
        elif isinstance(e, requests.exceptions.ConnectionError):
            raise XLDeployConnectionError('Could not connect to {0}'.format(self.config.host))
        elif isinstance(e, requests.exceptions.HTTPError):
            raise create_api_error_from_http_exception(e)
        else:
            raise e