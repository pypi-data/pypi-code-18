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

import requests
import base64
from nauth.clients.auth_client import AuthClient


class Auth0Client(AuthClient):
    @property
    def id_token_endpoint(self):
        if self._id_token_endpoint is None:
            return self.get_url_for_endpoint("/oauth/ro/")
        return self._id_token_endpoint

    @property
    def check_token_endpoint(self):
        if self._check_token_endpoint is None:
            return self.get_url_for_endpoint("/tokeninfo")
        return self._check_token_endpoint

    def get_email_code_endpoint(self):
        return self.get_url_for_endpoint("/passwordless/start")

    def get_sign_key(self):
        return base64.b64decode(
            self._client_secret
                .replace("_", "/")
                .replace("-", "+")
        )

    def get_id_token_data_payload(self, data):
        data = super(Auth0Client, self).set_id_token_data_payload(data)
        data["connection"] = data.get("connection",
                                      "Username-Password-Authentication")
        return data

    def send_auth_code_to_email(self, data):
        url = self.get_email_code_endpoint()
        ndata = {
            "connection": "email",
            "send:": "code",
            "email": data["username"],
            "client_id": data["client_id"],
        }
        requests.post(url, data=ndata)
