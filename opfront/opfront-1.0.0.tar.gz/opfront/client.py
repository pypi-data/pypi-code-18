from opfront.exceptions import BadRequestError, IntegrityError, ResourceNotFoundError, UnexpectedError

import requests


# TODO: Change to prod url
BASE_API_URL = "https://staging.opfront.ca"


class OpfrontClient(object):

    """
    OpfrontClient manages the login credentials as well as the token refresh flow

    Args:
        email (str): Email address with which to login
        password (str): Password associated with the email
    """

    def __init__(self, email, password):

        self._token = None
        self._refresh = None

        data = self.do_request('/auth/login', 'POST', body={'email': email, 'password': password})

        self._token = data['auth_token']
        self._refresh = data['refresh_token']

    @property
    def _headers(self):
        headers = {}
        if self._token:
            headers['X-Auth-Token'] = self._token

        return headers

    @classmethod
    def _validate_status_code(cls, resp):
        if resp.status_code == 404:
            raise ResourceNotFoundError()

        elif resp.status_code == 400:
            raise BadRequestError()

        elif resp.status_code == 422:
            raise IntegrityError()

        elif resp.status_code == 500:
            raise UnexpectedError()

        # TODO: Handle token expiration & refresh

    def do_request(self, url, method, body=None):
        """
        Perform a request to the Opfront API

        Args:
            url: Endpoint to query
            method: HTTP method
            body: Request payload

        Returns:
            dict: Response body

        """
        resp = None
        url = BASE_API_URL + url

        if method == 'GET':
            resp = requests.get(url, headers=self._headers)

        elif method == 'POST':
            resp = requests.post(url, json=body, headers={**self._headers, 'Content-Type': 'application/json'})

        elif method == 'PUT':
            resp = requests.put(url, json=body, headers={**self._headers, 'Content-Type': 'application/json'})

        elif method == 'DELETE':
            resp = requests.delete(url, headers=self._headers)

        if resp is None:
            raise ValueError('Invalid HTTP method: {}'.format(method))

        OpfrontClient._validate_status_code(resp)

        if resp.status_code == 204:
            return None

        return resp.json()['data']
