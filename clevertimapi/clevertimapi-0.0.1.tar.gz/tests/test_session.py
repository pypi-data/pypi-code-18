import json
from clevertimapi.session import Session, SessionError
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class FakeEndpoint(object):
    def __init__(self, session, key=None, lazy_load=False):
        pass


class TestSession(unittest.TestCase):

    def setUp(self):
        self.payload = {
            'id': 3434,
            'key1': 1,
            'key2': '2',
            'key3': [1, '2', [3]]
        }
        self.response = {
            'status': 'OK',
            'content': [
                self.payload
            ]
        }

    def test_get_without_register_fails(self):
        session = Session(api_key='APIKEY')
        with self.assertRaises(KeyError):
            session.get('FakeEndpoint', key=1, lazy_load=True)

    def test_enpoint_accepted_types(self):
        Session.register_endpoint(FakeEndpoint)
        accepted_types = Session.enpoint_accepted_types('FakeEndpoint')
        self.assertEqual(len(accepted_types), 1)
        self.assertTrue(accepted_types[0] is FakeEndpoint)
        Session.deregister_endpoint(FakeEndpoint)

    def test_is_registered_endpoint(self):
        self.assertFalse(Session.is_registered_endpoint(FakeEndpoint))
        self.assertFalse(Session.is_registered_endpoint(SessionError))
        self.assertFalse(Session.is_registered_endpoint('FakeEndpoint'))
        self.assertFalse(Session.is_registered_endpoint('SessionError'))
        Session.register_endpoint(SessionError)
        Session.register_endpoint(FakeEndpoint)
        self.assertTrue(Session.is_registered_endpoint(FakeEndpoint))
        self.assertTrue(Session.is_registered_endpoint(SessionError))
        self.assertTrue(Session.is_registered_endpoint('FakeEndpoint'))
        self.assertTrue(Session.is_registered_endpoint('SessionError'))
        Session.deregister_endpoint(SessionError)
        Session.deregister_endpoint(FakeEndpoint)
        self.assertFalse(Session.is_registered_endpoint(FakeEndpoint))
        self.assertFalse(Session.is_registered_endpoint(SessionError))
        self.assertFalse(Session.is_registered_endpoint('FakeEndpoint'))
        self.assertFalse(Session.is_registered_endpoint('SessionError'))
        self.assertFalse(Session.is_registered_endpoint(dict))

    def test_get_after_deregister_fails(self):
        session = Session(api_key='APIKEY')
        Session.register_endpoint(FakeEndpoint)
        Session.deregister_endpoint(FakeEndpoint)
        with self.assertRaises(KeyError):
            session.get('FakeEndpoint', key=1, lazy_load=True)

    def test_register_get(self):
        session = Session(api_key='APIKEY')
        Session.register_endpoint(FakeEndpoint)
        ret = session.get('FakeEndpoint', key=1, lazy_load=True)
        self.assertIsInstance(ret, FakeEndpoint)
        # second request hit the cache
        ret2 = session.get('FakeEndpoint', key=1, lazy_load=True)
        self.assertIsInstance(ret2, FakeEndpoint)
        self.assertTrue(ret is ret2)
        Session.deregister_endpoint(FakeEndpoint)

    def test_invalid_method_raises(self):
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
        with self.assertRaises(AssertionError):
            session.make_request(endpoint='/endpoint', resource_id=3434, method='INVALID')

    @mock.patch('requests.get')
    def test_make_request_get(self, mockRequestsGET):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsGET.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
        ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        self.assertEqual(ret, self.payload)
        mockRequestsGET.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY)

    @mock.patch('requests.get')
    def test_make_request_get_invalid_http_code_raises(self, mockRequestsGET):
        response = mock.Mock()
        response.status_code = 500
        response.text = json.dumps(self.response)
        mockRequestsGET.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
        with self.assertRaises(SessionError):
            session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')

    @mock.patch('requests.post')
    def test_make_request_post(self, mockRequestsPOST):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsPOST.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        ret = session.make_request(endpoint='endpoint', method='POST', payload=self.payload)
        self.assertEqual(ret, self.payload)
        mockRequestsPOST.assert_called_once_with('http://localhost:8000/fake/endpoint', headers=mock.ANY, data=json.dumps(self.payload, separators=(',', ':')))

    @mock.patch('requests.post')
    def test_make_request_post_invalid_http_code_raises(self, mockRequestsPOST):
        response = mock.Mock()
        response.status_code = 401
        response.text = json.dumps(self.response)
        mockRequestsPOST.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        with self.assertRaises(SessionError):
            session.make_request(endpoint='endpoint', method='POST', payload=self.payload)

    @mock.patch('requests.put')
    def test_make_request_put(self, mockRequestsPUT):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsPUT.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=self.payload)
        self.assertEqual(ret, self.payload)
        mockRequestsPUT.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY, data=json.dumps(self.payload, separators=(',', ':')))

    @mock.patch('requests.put')
    def test_make_request_put_invalid_http_code_raises(self, mockRequestsPUT):
        response = mock.Mock()
        response.status_code = 404
        response.text = json.dumps(self.response)
        mockRequestsPUT.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        with self.assertRaises(SessionError):
            session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=self.payload)

    @mock.patch('requests.delete')
    def test_make_request_delete(self, mockRequestsDELETE):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps({'status': 'OK'})
        mockRequestsDELETE.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        ret = session.make_request(endpoint='endpoint', resource_id='3434', method='DELETE', payload=None)
        self.assertEqual(ret, {'status': 'OK'})
        mockRequestsDELETE.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY)

    @mock.patch('requests.delete')
    def test_make_request_delete_invalid_http_code_raises(self, mockRequestsDELETE):
        response = mock.Mock()
        response.status_code = 470
        response.text = json.dumps({'status': 'OK'})
        mockRequestsDELETE.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        with self.assertRaises(SessionError):
            session.make_request(endpoint='endpoint', resource_id='3434', method='DELETE', payload=None)

    @mock.patch('requests.get')
    def test_caching_enabled_2nd_get_hits_cache(self, mockRequestsGET):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsGET.return_value = response

        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=True)
        ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        self.assertIsNotNone(ret)
        # 2nd request should hit the cache
        ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        mockRequestsGET.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY)
        self.assertTrue(ret is ret2)

    @mock.patch('requests.get')
    def test_caching_enabled_2nd_get_with_reload_hits_server(self, mockRequestsGET):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsGET.return_value = response

        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=True)
        ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        self.assertIsNotNone(ret)
        # 2nd request should hit the cache
        ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET', reload=True)
        self.assertEqual(mockRequestsGET.call_count, 2)
        self.assertTrue(ret is not ret2)
        self.assertEqual(ret, ret2)

    @mock.patch('requests.get')
    def test_caching_disabled_2nd_get_hits_server(self, mockRequestsGET):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsGET.return_value = response

        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=False)
        ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        self.assertIsNotNone(ret)
        # 2nd request should hit the cache
        ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
        self.assertEqual(mockRequestsGET.call_count, 2)
        self.assertTrue(ret is not ret2)
        self.assertEqual(ret, ret2)

    @mock.patch('requests.post')
    def test_cache_enabled_post_updates_the_cache(self, mockRequestsPOST):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsPOST.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        self.assertIsNone(session._get_cached_value(endpoint='endpoint', resource_id=3434))
        ret = session.make_request(endpoint='endpoint', method='POST', payload=self.payload)
        self.assertEqual(ret, self.payload)
        self.assertEqual(session._get_cached_value(endpoint='endpoint', resource_id=3434), self.payload)
        mockRequestsPOST.assert_called_once_with('http://localhost:8000/fake/endpoint', headers=mock.ANY, data=json.dumps(self.payload, separators=(',', ':')))
        # now a get without reload, should return from the cache
        ret = session.make_request(endpoint='endpoint', resource_id=self.payload['id'], method='GET')
        self.assertEqual(ret, self.payload)

    @mock.patch('requests.put')
    def test_cache_enabled_put_updates_the_cache(self, mockRequestsPUT):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsPUT.return_value = response
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        self.assertIsNone(session._get_cached_value(endpoint='endpoint', resource_id=3434))
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=self.payload)
        self.assertEqual(ret, self.payload)
        self.assertEqual(session._get_cached_value(endpoint='endpoint', resource_id=3434), self.payload)
        mockRequestsPUT.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY, data=json.dumps(self.payload, separators=(',', ':')))
        # now a get without reload, should return from the cache
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='GET')
        self.assertEqual(ret, self.payload)

    @mock.patch('requests.delete')
    @mock.patch('requests.put')
    def test_cache_enabled_delete_clears_the_cache(self, mockRequestsPUT, mockRequestsDELETE):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.response)
        mockRequestsPUT.return_value = response
        response2 = mock.Mock()
        response2.status_code = 200
        response2.text = json.dumps({'status': 'OK'})
        mockRequestsDELETE.return_value = response2
        session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
        self.assertIsNone(session._get_cached_value(endpoint='endpoint', resource_id=3434))
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=self.payload)
        self.assertEqual(ret, self.payload)
        self.assertEqual(session._get_cached_value(endpoint='endpoint', resource_id=3434), self.payload)
        mockRequestsPUT.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers=mock.ANY, data=json.dumps(self.payload, separators=(',', ':')))
        # now a get without reload, should return from the cache
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='GET')
        self.assertEqual(ret, self.payload)
        # now a delete should clear the cache
        ret = session.make_request(endpoint='endpoint', resource_id=3434, method='DELETE')
        self.assertIsNone(session._get_cached_value(endpoint='endpoint', resource_id=3434))
