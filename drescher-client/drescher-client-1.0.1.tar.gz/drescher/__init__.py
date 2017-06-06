# coding: utf-8

from __future__ import print_function
from copy import deepcopy

import requests
from six.moves.urllib.parse import urljoin

from drescher import endpoints
from drescher.models import Unit

__version__ = '1.0.1'


DRESCHER_API = 'https://upload.drescher.hu/api/'


class Drescher(object):
    def __init__(self, username, api_key, api=DRESCHER_API):
        """
        :type username: str
        :type api_key: str
        :type api: str
        """
        
        self._auth = {
            'username': username,
            'api_key': api_key
        }
        self._api = api

    def _post(self, endpoint, json=None, **kwargs):
        """
        :type endpoint: str
        :type json: dict
        :type kwargs: dict
        :param kwargs: Any keyword argument that can be passed to `requests.post()`
        :rtype: dict
        """

        url = urljoin(self._api, endpoint.lstrip('/'))

        if json is None:
            json = {}
        else:
            json = deepcopy(json)
        json.update(self._auth)

        reply = requests.post(url, json=json, **kwargs)
        reply.raise_for_status()

        return reply.json()

    def _get(self, endpoint, params=None, **kwargs):
        """
        :type endpoint: str
        :type params: dict
        :type kwargs: dict
        :param kwargs: Any keyword argument that can be passed to `requests.get()`
        :rtype: dict
        """

        url = urljoin(self._api, endpoint.lstrip('/'))

        if params is None:
            params = {}
        else:
            params = deepcopy(params)
        params.update(self._auth)

        reply = requests.get(url, params=params, **kwargs)
        reply.raise_for_status()

        return reply.json()

    def get_unit_list(self):
        """
        :return: Unit
        """
        for unit in self._get(endpoints.UNIT_LIST):
            yield Unit(unit)
