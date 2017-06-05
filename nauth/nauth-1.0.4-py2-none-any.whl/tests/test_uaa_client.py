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

import pytest
import json
from nauth.clients.auth_client import AuthClientConfig
from nauth.clients.uaa_client import UaaClient


class MockResponse(object):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.text = json.dumps(json_data)
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.fixture
def post(monkeypatch, value):
    class FakePost(object):
        def __init__(self, url="", data="", auth=""):
            self.url = url
            self.data = data
            self.auth = auth

    fp = FakePost()

    def get_post(url, data, auth):
        fp.data = data
        return value

    monkeypatch.setattr('requests.post', get_post)
    return fp


@pytest.fixture(scope='module')
def uaa_client():
    auth_config = AuthClientConfig(
        client_id="test",
        client_secret="test",
        auth_host="http://test")
    client = UaaClient(auth_config)
    return client


@pytest.mark.parametrize("value", [MockResponse({"email": "Test"}, 200)])
def test_get_check_token_response_returns_tenant(post, uaa_client):
    """
    get_check_token_response() should return default tenant Nervana Systems
    """
    token_payload = uaa_client.get_check_token_response("")

    assert (token_payload.tenant == "Nervana Systems")


@pytest.mark.parametrize("value", [MockResponse({"id_token": "Test"}, 200)])
def test_get_id_token_request(post, uaa_client):
    """
    get_id_token() should set response_type to id_token
    """
    data = {}

    uaa_client.get_id_token(data)
    expected = {
        "client_id": "test",
        "client_secret": "test",
        "scope": "openid",
        "grant_type": "password",
        "response_type": "id_token"
    }

    assert (post.data == expected)
