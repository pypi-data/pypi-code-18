import json

import logging
import pprint
import random
import string

from tornado.testing import AsyncHTTPTestCase

logger = logging.getLogger("testing.case")

class TestCaseError(Exception):
    pass

class APITestCase(AsyncHTTPTestCase):

    def get_settings(self):
        raise NotImplemented

    def generate_random_string(self, N):
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(N))

    @property
    def qap_api_url(self):
        return self.get_settings()["qap_api_url"]

    def fetch_ext(self, url, **kwargs):
        self.http_client.fetch(
            url,
            self.stop,
            **kwargs
        )

        return self.wait()

    def load_body(self, response):
        return json.loads(response.body.decode("utf-8"))

    def prettify(self, data):
        return pprint.pformat(data)

    def ensure_success(self, response):
        if response.code < 200 or response.code > 299:
            logger.error("API request failed.")
            logger.error(self.prettify(self.load_body(response)))
            raise TestCaseError

    def create_token(self, username, password, ensure_success=True):
        response = self.fetch_ext(
            self.qap_api_url + '/api/tokens',
            method='POST',
            body=json.dumps({
                "username": username,
                "password": password
            })
        )

        if ensure_success:
            self.ensure_success(response)

        return self.load_body(response)["token"]

    def create_membership(self, data, ensure_success=True):
        default_membership = {
                "_id": "cnnturk",
                "name": "CNNTurk",
                "username": "yusuf.sahin",
                "password": "brm_hy81"
        }

        default_membership.update(data)

        response = self.fetch_ext(
            self.qap_api_url + '/membership',
            method='POST',
            body=json.dumps(default_membership)
        )

        if ensure_success:
            self.ensure_success(response)

        self.membership = self.load_body(response)
        self.membership_creator_token = self.get_token_of(
            default_membership["username"], default_membership["password"])


    def create_user(self, data, ensure_success=True):
        default_user = {
            "username": "erdem.guner",
            "passowrd": "brm_hy81",
            "permissions": [],
            "domains": []
        }

        default_user.update(data)

        response = self.fetch_ext(
            '/api/users',
            method='POST',
            headers=self.get_auth_header(self.membership_creator_token),
            body=json.dumps(default_user)
        )

        if ensure_success:
            self.ensure_success(response)

        return response

    def create_domain(self, data, ensure_success=True):
        default_domain = {
            "name": self.generate_random_string(10)
        }

        default_domain.update(data)

        response = self.fetch_ext(
            self.qap_api_url + '/api/domains',
            method='POST',
            headers=self.get_auth_header(self.membership_creator_token),
            body=json.dumps(default_domain)
        )

        if ensure_success:
            self.ensure_success(response)

        return response

    def create_permission_group(self, data, ensure_success=True):
        default_permission_group = {
            "name": self.generate_random_string(10),
            "permissions": []
        }

        default_permission_group.update(data)

        response = self.fetch_ext(
            self.qap_api_url + '/api/permission-groups',
            method='POST',
            body=json.dumps(data),
            headers=self.get_auth_header(self.membership_creator_token)
        )

        if ensure_success:
            self.ensure_success(response)

        return response


    def test_create(self):
        self.get_membership_owner_token()





if __name__ == '__main__':
    test_case = APITestCase()
    test_case.run()


