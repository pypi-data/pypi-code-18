"""
arcgis-sdk
~~~~~~~~~~
Python SDK for Arcgis API
:copyright: (c) 2017 mongkok
:license: MIT, see LICENSE for more details
"""

import requests


__version__ = '0.0.3'

ARCGIS_API_URL = 'https://www.arcgis.com/sharing/rest/'


class ArcgisAPI(object):
    """
    Docs: https://resources.arcgis.com/en/help/arcgis-rest-api/
    """

    def __init__(self, access_token, timeout=None,
                 proxies=None, session=None):

        self.access_token = access_token
        self.timeout = timeout
        self.proxies = proxies
        self.session = session or requests.Session()

    def refresh_token(self, client_id, refresh_token):
        result = self.request('oauth2/token/', {
            'client_id': client_id,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        })

        self.access_token = result.get('access_token')
        return result

    def self(self):
        return self.request('portals/self')

    def users(self, **params):
        return self.request(
            'community/users',
            params=params)

    def user_detail(self, username):
        return self.request(
            "community/users/{username}".format(username=username))

    def groups(self, **params):
        return self.request(
            'community/groups',
            params=params)

    def create_group(self, **data):
        return self.post(
            'community/createGroup',
            data=data)

    def group_detail(self, group_id):
        return self.request(
            "community/groups/{group_id}".format(group_id=group_id))

    def update_group(self, group_id, **data):
        return self.post(
            "community/groups/{group_id}/update".format(group_id=group_id),
            data=data)

    def delete_group(self, group_id):
        return self.post(
            "community/groups/{group_id}/delete".format(group_id=group_id))

    def add_users_to_group(self, group_id, users):
        return self.post(
            "community/groups/{group_id}/addUsers".format(group_id=group_id),
            data={'users': users})

    def invite_to_group(self, group_id, **data):
        return self.post(
            "community/groups/{group_id}/invite".format(group_id=group_id),
            data=data)

    def add_item(self, username, **data):
        return self.post(
            "content/users/{username}/addItem".format(username=username),
            data=data)

    def post(self, *args, **kwargs):
        return self.request(method='POST', *args, **kwargs)

    def request(self, path, params=None, data=None, files=None, method=None):
        if params is None:
            params = dict()

        if params.get('grant_type') != 'refresh_token':
            params.update({
                'token': self.access_token,
                'f': 'json'
            })

        response = self.session.request(
            method or 'GET',
            ARCGIS_API_URL + path,
            data=data,
            params=params,
            proxies=self.proxies,
            timeout=self.timeout,
            files=files)

        if not 200 <= response.status_code < 300:
            raise ArcgisAPIError(code=response.status_code)

        result = response.json()

        if result.get('error'):
            raise ArcgisAPIError(result)
        return result


class ArcgisAPIError(Exception):

    def __init__(self, result=None, code=None):
        self.result = result

        if isinstance(result, dict):
            self.code = result['error']['code']
            self.details = result['error']['details']
            self.message = result['error']['message']
        else:
            self.code = code
            self.message = 'Server error'

        Exception.__init__(self, self.message)
