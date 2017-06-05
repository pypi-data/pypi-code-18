# ----------------------------------------------------------------------------
# Copyright 2015-2017 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
#
# # -*- coding: utf-8 -*-

import logging
import requests
from requests.auth import HTTPBasicAuth

from nauth.clients.auth_client import AuthClient, AuthCheckTokenPayload

logger = logging.getLogger()


class UaaClient(AuthClient):
    def __init__(self, auth_client_config):
        AuthClient.__init__(self, auth_client_config)
        self._sign_key = None

    @property
    def id_token_endpoint(self):
        if self._id_token_endpoint is None:
            return self.get_url_for_endpoint("/oauth/token/")
        return self._id_token_endpoint

    @property
    def check_token_endpoint(self):
        if self._check_token_endpoint is None:
            return self.get_url_for_endpoint("/check_token")
        return self._check_token_endpoint

    def get_sign_key(self):
        if self._sign_key is None:
            auth = self._get_auth()
            token_key_url = self.get_url_for_endpoint("/token_key")
            res = requests.get(token_key_url, auth=auth)
            payload = AuthClient.get_json_payload(res)
            self._sign_key = payload["value"]
        return self._sign_key

    def get_id_token_data_payload(self, data):
        data = super(UaaClient, self).set_id_token_data_payload(data)
        return data

    def _make_id_token_request(self, data):
        auth = self._get_auth()
        url = self.id_token_endpoint
        return requests.post(url, data=data, auth=auth)

    def _make_check_token_request(self, token):
        auth = self._get_auth()
        data = {"token": token}
        url = self.check_token_endpoint
        res = requests.post(url, data=data, auth=auth)
        return res

    def _get_auth(self):
        return HTTPBasicAuth(self._client_id, self._client_secret)

    def get_check_token_response(self, token):
        res = self._make_check_token_request(token)

        if res.status_code == 200:
            res = AuthClient.get_json_payload(res)
            return AuthCheckTokenPayload(
                email=res["email"],
                tenant="Nervana Systems"
            )

        logger.error(res.text)
        logger.error("Unable to check token {}".format(token))

        return None
