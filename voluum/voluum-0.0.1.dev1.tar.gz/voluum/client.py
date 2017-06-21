import json
from urlparse import urljoin

import requests

from django.conf import settings


class Client(object):

    api = 'https://api.voluum.com'
    auth_header_name = 'cwauth-token'
    auth_path = '/auth/session'
    campaign_list_path = '/campaign'
    aggregated_report_path = '/report/aggregated/{unit}'

    def __init__(self, *args, **kwargs):
        self.settings = getattr(settings, 'VOLUUM', {})

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }
        if getattr(self, 'token', None):
            headers[self.auth_header_name] = self.token
        return headers

    def post(self, path, data):
        url = urljoin(self.api, path)
        headers = self.get_headers()
        return requests.post(url, data=json.dumps(data), headers=headers)

    def get(self, path, params=None):
        url = urljoin(self.api, path)
        headers = self.get_headers()
        return requests.get(url, params=params, headers=headers)

    def authenticate(self, email=None, password=None):
        response = self.post(self.auth_path, {
            "email": email or self.settings.get('EMAIL'),
            "password": password or self.settings.get('PASSWORD')
        })
        if response.status_code == 200:
            self.token = response.json().get('token')

    def get_campaign_list(self):
        response = self.get(self.campaign_list_path)
        return response.json().get('campaigns', [])

    def get_aggregated_report(
        self,
        campaign_id,
        unit='DAY',
        date_from=None,
        date_to=None
    ):
        path = self.aggregated_report_path.format(unit=unit)

        params = {
            'filter1': 'campaignId',
            'filter1Value': campaign_id
        }
        if date_from:
            params['from'] = date_from.isoformat()
        if date_to:
            params['to'] = date_to.isoformat()

        response = self.get(path, params=params)
        return response.json()
