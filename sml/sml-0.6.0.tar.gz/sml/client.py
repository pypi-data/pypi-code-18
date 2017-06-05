"""Interact with a SherlockML service."""

# Copyright 2017 ASI Data Science
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import requests

import sml.auth
import sml.version


class SherlockMLServiceError(Exception):
    """Exception for errors interacting with a SherlockML service."""

    pass


class ServerSentEventMessage(object):
    """A message from a server sent event stream."""

    def __init__(self, id_, event, data):
        self.id_ = id_
        self.event = event
        self.data = data

    @classmethod
    def from_lines(cls, lines):
        id_ = None
        event = None
        data_lines = []
        for line in lines:
            if line.startswith('id:'):
                id_ = int(line[3:].strip())
            elif line.startswith('event:'):
                event = line[6:].strip()
            elif line.startswith('data:'):
                data_lines.append(line[5:].strip())
            else:
                raise ValueError('unexpected sse line: {}'.format(line))
        data = json.loads('\n'.join(data_lines))
        return cls(id_, event, data)


class SherlockMLService(object):
    """A client for interacting with a SherlockML service."""

    def __init__(self, url, cookie_auth=False):
        self.url = url
        self.cookie_auth = cookie_auth

    @property
    def _headers(self):
        headers = {'User-Agent': sml.version.user_agent()}
        if not self.cookie_auth:
            headers.update(sml.auth.auth_headers())
        return headers

    @property
    def _cookies(self):
        cookies = {}
        if self.cookie_auth:
            cookies['token'] = sml.auth.token()
        return cookies

    def _check_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                msg = response.json().get('error', '')
            except Exception:  # pylint: disable=broad-except
                msg = 'error from the server'
            raise SherlockMLServiceError(msg)

    def _get(self, endpoint, params=None):
        url = '{}{}'.format(self.url, endpoint)
        response = requests.get(url, headers=self._headers,
                                cookies=self._cookies, params=params)
        self._check_response(response)
        return response

    def _delete(self, endpoint, params=None):
        url = '{}{}'.format(self.url, endpoint)
        response = requests.delete(url, headers=self._headers,
                                   cookies=self._cookies, params=params)
        self._check_response(response)
        return response

    def _post(self, endpoint, payload, params=None):
        url = '{}{}'.format(self.url, endpoint)
        response = requests.post(
            url, headers=self._headers, cookies=self._cookies, json=payload,
            params=params
        )
        self._check_response(response)
        return response

    def _put(self, endpoint, payload=None, params=None):
        url = '{}{}'.format(self.url, endpoint)
        response = requests.put(
            url, headers=self._headers, cookies=self._cookies, json=payload,
            params=params
        )
        self._check_response(response)
        return response

    def _stream(self, endpoint):
        response = self._get(endpoint, params={'stream': True})
        buf = []
        for line in response.iter_lines(decode_unicode=True):
            if not line.strip():
                yield ServerSentEventMessage.from_lines(buf)
                buf = []
            else:
                buf.append(line)
