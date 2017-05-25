from clevertimapi.endpoint import Endpoint
from clevertimapi.session import Session
from clevertimapi.user import Group
import json
from mock_utils import setup_requests_call_mock
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        self.session = Session('API_KEY')

        # just so we can test with this class
        Endpoint.ENDPOINT = '/fake'

        self.payload = {
            'status': 'OK',
            'content': [{
                'id': 6789,
                'is_private': True,
                'gid': 2 + 4 + 64,
                'ao': 'now',
                'lm': '2017-01-04T10:23:22Z',
            }]
        }

    def _setup_GET_mock(self, key):
        self.payload['content'][0]['id'] = key

        self.mockRequestsGET = mock.patch('requests.get').start()
        setup_requests_call_mock(self.mockRequestsGET, {
            '/fake/%s' % key: (200, json.dumps(self.payload, separators=(',', ':')))
        })
        self.group1 = {
            'id': 34,
            'name': 'Sales Users',
            'gid': 2,
            'users': [34, 89, 788]
        }
        self.group2 = {
            'id': 46,
            'name': 'External Users',
            'gid': 4,
            'users': [12, 101]
        }
        self.group3 = {
            'id': 77,
            'name': 'Marketing Users',
            'gid': 16,
            'users': [55]
        }
        self.group4 = {
            'id': 98,
            'name': 'Field Engineers',
            'gid': 64,
            'users': [122, 123, 124]
        }
        setup_requests_call_mock(self.mockRequestsGET, {
            '/group': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.group1,
                        self.group2,
                        self.group3,
                        self.group4
                    ]
                })
            )
        })

    def tearDown(self):
        mock.patch.stopall()

    def test_lazy_load_loads_on_first_property(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session, key=1234, lazy_load=True)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_unlazy_load_loads_in_init(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session, key=1234, lazy_load=False)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_lazy_load_reload(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session, key=1234, lazy_load=True)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        endpoint.reload()
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_unlazy_load_reload(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session, key=1234, lazy_load=False)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        endpoint.reload()
        self.assertEqual(self.mockRequestsGET.call_count, 2)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 2)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(self.mockRequestsGET.call_count, 2)

    def test_reload_on_new_lazy_endpoint_fails(self):
        endpoint = Endpoint(self.session, lazy_load=True)
        with self.assertRaises(AssertionError):
            endpoint.reload()

    def test_reload_on_new_unlazy_endpoint_fails(self):
        endpoint = Endpoint(self.session, lazy_load=False)
        with self.assertRaises(AssertionError):
            endpoint.reload()

    def test_new_endpoints_do_not_call_get_on_properties(self):
        properties = [prop for prop in dir(Endpoint) if isinstance(getattr(Endpoint, prop), property)]
        for prop in properties:
            endpoint = Endpoint(self.session, lazy_load=True)
            getattr(endpoint, prop)
            endpoint2 = Endpoint(self.session, lazy_load=False)
            getattr(endpoint2, prop)

    def test_lazy_instance_loads_on_any_first_property_except_key(self):
        properties = [prop for prop in dir(Endpoint) if isinstance(getattr(Endpoint, prop), property)]
        key = 123
        for prop in properties:
            self._setup_GET_mock(key)
            endpoint = Endpoint(self.session, key=key, lazy_load=True)
            self.assertEqual(self.mockRequestsGET.call_count, 0)
            getattr(endpoint, prop)
            if prop == 'key':
                self.assertEqual(self.mockRequestsGET.call_count, 0)
            else:
                self.assertEqual(self.mockRequestsGET.call_count, 1)
            key += 1

    @mock.patch('requests.put')
    def test_save_existing_endpoint(self, mockRequestsPUT):
        self._setup_GET_mock(6789)
        setup_requests_call_mock(mockRequestsPUT, {
            '/fake/6789': (200, json.dumps(self.payload))
        })

        endpoint = Endpoint(self.session, key=6789, lazy_load=False)
        endpoint.save()

        self.assertEqual(mockRequestsPUT.call_count, 1)
        session_url = mockRequestsPUT.call_args_list[0][0][0]
        data = mockRequestsPUT.call_args_list[0][1]['data']
        self.assertEqual(session_url, Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789')
        self.assertEqual(json.loads(data), self.payload['content'][0])

    @mock.patch('requests.post')
    def test_save_new_endpoint(self, mockRequestsPOST):
        setup_requests_call_mock(mockRequestsPOST, {
            '/fake': (200, json.dumps(self.payload))
        })

        endpoint = Endpoint(self.session)
        self.assertTrue(endpoint.is_new())
        endpoint.save()

        self.assertEqual(mockRequestsPOST.call_count, 1)
        session_url = mockRequestsPOST.call_args_list[0][0][0]
        data = mockRequestsPOST.call_args_list[0][1]['data']
        self.assertEqual(session_url, Session.ENDPOINT_URL + Endpoint.ENDPOINT)
        self.assertEqual(json.loads(data), {})

        self.assertFalse(endpoint.is_new())
        self.assertEqual(endpoint.key, 6789)

    @mock.patch('requests.delete')
    def test_delete_unlazy_loaded_endpoint(self, mockRequestsDELETE):
        self._setup_GET_mock(6789)
        setup_requests_call_mock(mockRequestsDELETE, {
            '/fake/6789': (200, json.dumps(self.payload))
        })

        endpoint = Endpoint(self.session, key=6789, lazy_load=False)
        endpoint.delete()

        mockRequestsDELETE.assert_called_once_with(Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789', headers=mock.ANY)
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    @mock.patch('requests.delete')
    def test_delete_lazy_loaded_endpoint(self, mockRequestsDELETE):
        setup_requests_call_mock(mockRequestsDELETE, {
            '/fake/6789': (200, json.dumps(self.payload))
        })

        endpoint = Endpoint(self.session, key=6789, lazy_load=True)
        endpoint.delete()

        mockRequestsDELETE.assert_called_once_with(Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789', headers=mock.ANY)

    def test_groups_get(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session, key=1234, lazy_load=True)
        self.assertEqual(endpoint.get_groups(), (
            Group(self.session, key=34),
            Group(self.session, key=46),
            Group(self.session, key=98),
        ))

    def test_groups_set(self):
        self._setup_GET_mock(1234)
        endpoint = Endpoint(self.session)
        groups = [Group(self.session, key=34), Group(self.session, key=46)]
        endpoint.set_groups(groups)
        self.assertEqual(endpoint.get_content().get('gid'), 2 + 4)
        self.assertEqual(endpoint.get_groups(), (
            Group(self.session, key=34),
            Group(self.session, key=46),
        ))
