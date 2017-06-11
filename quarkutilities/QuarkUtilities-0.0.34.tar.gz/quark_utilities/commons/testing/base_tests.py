import functools
import json
from urllib.parse import urljoin

import bcrypt
import pymongo

from quark_utilities import json_helpers
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.testing import AsyncHTTPTestCase

from quark_utilities.commons.testing.object_mother import ObjectMother

class TestConfigurationError(Exception):
    pass


class QuarkBase(AsyncHTTPTestCase):

    DEFAULT_SETTINGS = {
        "secret": bcrypt.gensalt(),
        "token_ttl": 30000,
        "token_issuer": "TestManager",
        "mongo_connection_string": "localhost",
        "mongo_default_db": "quark_test",
        "save_events": True
    }

    def setUp(self):
        super(QuarkBase, self).setUp()
        self.object_mother = ObjectMother(pymongo.MongoClient("localhost"))
        self.object_mother.drop()

        for on_start_func in self.flasky_app.on_start_funcs:
            IOLoop.current().run_sync(functools.partial(on_start_func, self.flasky_app))

        if hasattr(self, "before_t"):
            self.before_t()

    def get_new_ioloop(self):
        self._io_loop = AsyncIOMainLoop()
        return self._io_loop

    def get_app(self):
        self.flasky_app = self.get_flasky_app()
        self.flasky_app.build_app()
        return self.flasky_app.app

    def get_settings(self):
        return self.DEFAULT_SETTINGS

    def fetch_ext(self, url, **kwargs):
        self.http_client.fetch(
            url,
            self.stop,
            **kwargs
        )

        return self.wait()

    def assertErrorCodeEquals(self, response, code, msg=None):
        body = self.load_body(response)
        self.assertEquals(body["error"]["code"], code, msg=msg)

    def load_body(self, response):
        return json.loads(response.body.decode("utf-8"))

    def craft_fields(self):
        data = {}
        for key, val in self.required_fields:
            data[key] = val
        return data




class ResourceCreationCase(QuarkBase):

    def do_post(self, body):
        headers = {}

        if hasattr(self, "token"):
            headers.update({
                "Authorization": "Bearer " + self.token
            })

        return self.fetch(
            self.resource_url,
            method='POST',
            headers=headers,
            body=json.dumps(body)
        )

    def test_201(self):
        response = self.do_post(body=self.craft_fields())

        self.assertEquals(response.code, 201)
        ret = json.loads(response.body.decode("utf-8"))
        self.assertIsNotNone(ret["_id"])
        self.assertIsNotNone(ret["sys"])
        self.assertIsNotNone(ret["sys"]["created_at"])
        self.assertIsNotNone(ret["sys"]["created_by"])
        self.assertIsNotNone(ret["sys"]["cid"])


    def test_400(self):
        for key, _ in self.required_fields:
            body = self.craft_fields()

            body.pop(key, None)

            response = self.do_post(body=body)

            self.assertEquals(response.code, 400)
            self.assertErrorCodeEquals(response, "errors.parameterRequired")

    def test_403(self):
        if not hasattr(self, "civil_token"):
            return

        response = self.do_post(body=self.craft_fields())
        self.assertEquals(response.code, 403)
        self.assertErrorCodeEquals(response, "errors.agentIsNotAuthorized")

    def test_409(self):
        body = self.craft_fields()

        response = self.do_post(body=body)
        self.assertEquals(response.code, 201)

        response = self.do_post(body=body)
        self.assertEquals(response.code, 409)


class ResourceUpdateCase(QuarkBase):

    def do_put(self, _id, body, token):
        headers = {
            "Authorization": "Bearer " + token
        }

        return self.fetch(
            urljoin(self.resource_url,str(_id)),
            method='PUT',
            headers=headers,
            body=json.dumps(body, default=json_helpers.bson_to_json)
        )

    def test_200(self):
        resource = self.resource
        resource["test_key"] = "test_val"

        response = self.do_put(resource["_id"], resource, self.token)

        self.assertEquals(response.code, 200)
        ret = json.loads(response.body.decode("utf-8"))
        self.assertIsNotNone(ret["_id"])
        self.assertEquals(ret["test_key"], "test_val")
        self.assertIsNotNone(ret["sys"])
        self.assertIsNotNone(ret["sys"]["created_at"])
        self.assertIsNotNone(ret["sys"]["created_by"])
        self.assertIsNotNone(ret["sys"]["cid"])
        self.assertIsNotNone(ret["sys"]["modified_at"])
        self.assertIsNotNone(ret["sys"]["modified_by"])

    def test_403(self):
        if hasattr(self, "tests") and "403" not in self.tests:
            self.skipTest("Not running")

        if not hasattr(self, "token"):
            raise TestConfigurationError("This test requires token...")

        self.object_mother.create_user_civil()
        token = self.object_mother.create_civil_token(self.DEFAULT_SETTINGS["secret"])

        response = self.do_put(self.resource["_id"], self.resource, token)

        self.assertEquals(response.code, 403)

        code = getattr(self, "error_code_403", "errors.notAuthorized")
        self.assertErrorCodeEquals(response, code)


class ResourceDeleteCase(QuarkBase):

    def do_delete(self, _id, token):
        headers = {
            "Authorization": "Bearer " + token
        }

        return self.fetch(
            urljoin(self.resource_url, str(_id)),
            method='DELETE',
            headers=headers
        )

    def test_204(self):
        if hasattr(self, "tests") and "204" not in self.tests:
            self.skipTest("Not running")

        if not hasattr(self, "token"):
            raise TestConfigurationError("This test requires token...")

        response = self.do_delete(self.resource_id, token=self.token)

        self.assertEquals(response.code, 204)

    def test_404(self):
        if hasattr(self, "tests") and "404" not in self.tests:
            self.skipTest("Not running")

        if not hasattr(self, "token"):
            raise TestConfigurationError("This test requires token...")


        response = self.do_delete("123456789", token=self.token)
        self.assertEquals(response.code, 404)

    def test_403(self):
        if hasattr(self, "tests") and "403" not in self.tests:
            self.skipTest("Not running")

        self.object_mother.create_user_civil()
        token = self.object_mother.create_civil_token(self.DEFAULT_SETTINGS["secret"])

        response = self.do_delete(self.resource_id, token=token)
        self.assertEquals(response.code, 403)



class ResourceFindCase(QuarkBase):

    def test_200(self):
        if hasattr(self, "tests") and "200" not in self.tests:
            self.skipTest("Not running")

        if not hasattr(self, "token"):
            raise TestConfigurationError("This test requires token...")

        headers = {
            "Authorization": "Bearer " + self.token
        }

        response = self.fetch(
            urljoin(self.resource_url, str(self.resource_id)),
            headers=headers
        )

        print(response.body)
        self.assertEquals(response.code, 200)

        ret = json.loads(response.body.decode("utf-8"))
        self.assertEquals(ret["_id"], self.resource_id)

    def test_403(self):
        if hasattr(self, "tests") and "403" not in self.tests:
            self.skipTest("Not running")

        self.object_mother.create_user_civil()
        token = self.object_mother.create_civil_token(self.DEFAULT_SETTINGS["secret"])

        headers = {
            "Authorization": "Bearer " + token
        }

        response = self.fetch(
            urljoin(self.resource_url, str("1234567890")),
            headers=headers
        )

        code = "errors.notAuthorized"
        if hasattr(self, "error_code_403"):
            code = self.error_code_403

        self.assertEquals(response.code, 403)
        self.assertErrorCodeEquals(response, code)


    def test_404(self):
        if hasattr(self, "tests") and "404" not in self.tests:
            self.skipTest("Not running")

        if not hasattr(self, "token"):
            raise TestConfigurationError("This test requires token...")

        headers = {
            "Authorization": "Bearer " + self.token
        }

        response = self.fetch(
            urljoin(self.resource_url, str("1234567890")),
            headers=headers
        )

        self.assertEquals(response.code, 404)
        self.assertErrorCodeEquals(response, "errors.resourceNotFound")