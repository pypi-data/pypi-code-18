from unittest import TestCase

from rancon import app


class TestHTTPEndpoints(TestCase):

    def test_index_returns_200(self):
        request, response = app.test_client.get("/")
        self.assertEqual(200, response.status)
