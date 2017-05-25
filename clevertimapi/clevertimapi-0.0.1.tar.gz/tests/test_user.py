import json
from clevertimapi.session import Session
from clevertimapi.user import User, Group
from mock_utils import setup_requests_call_mock
import sys
try:
    import unittest.mock as mock
except ImportError:
    import mock
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestFile(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')

        self.mockRequestsGET = mock.patch('requests.get').start()
        setup_requests_call_mock(self.mockRequestsGET, {
            '/user': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        {
                            'id': 11,
                            'user': 'Mike Zorillo',
                            'email': 'mike.zorillo@gmail.com',
                            'is_owner': False,
                            'is_admin': False,
                            'permissions': ['canexport', 'canedit'],
                            'pending': False
                        },
                        {
                            'id': 12,
                            'user': 'John Cash',
                            'email': 'john.cash@yahoo.com',
                            'is_owner': False,
                            'is_admin': True,
                            'permissions': ['canexport', 'canedit', 'candelete'],
                            'pending': False
                        },
                        {
                            'id': 13,
                            'user': 'Donald Duck',
                            'email': 'donald.duck@disney.com',
                            'is_owner': True,
                            'is_admin': True,
                            'permissions': ['canexport', 'canedit', 'candelete'],
                            'pending': False
                        }
                    ]
                })
            ),
            '/group': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        {
                            'id': 5,
                            'name': 'Marketing Users',
                            'gid': 2,
                            'users': [11],
                        },
                        {
                            'id': 6,
                            'name': 'Sales Users',
                            'gid': 4,
                            'users': [12, 13]
                        },
                        {
                            'id': 7,
                            'name': 'Internal Users',
                            'gid': 8,
                            'users': [11, 12, 13]
                        }
                    ]
                })
            )
        })

    def tearDown(self):
        mock.patch.stopall()

    def test_load_all_users_on_single_request(self):
        user = User(self.session, key=12)
        self.mockRequestsGET.assert_called_once_with(Session.ENDPOINT_URL + '/user', headers=mock.ANY)
        self.assertEqual(user.key, 12)
        self.assertEqual(user.name, 'John Cash')
        self.assertEqual(user.email, 'john.cash@yahoo.com')
        self.assertEqual(user.is_owner, False)
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.permissions, ['canexport', 'canedit', 'candelete'])
        self.assertEqual(user.registration_pending, False)

        # another load will not go to the server, but hit the cache
        user = User(self.session, key=13)
        self.mockRequestsGET.assert_called_once_with(Session.ENDPOINT_URL + '/user', headers=mock.ANY)
        self.assertEqual(user.key, 13)
        self.assertEqual(user.name, 'Donald Duck')
        self.assertEqual(user.email, 'donald.duck@disney.com')
        self.assertEqual(user.is_owner, True)
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.permissions, ['canexport', 'canedit', 'candelete'])
        self.assertEqual(user.registration_pending, False)

    def test_load_all_groups_on_single_request(self):
        group = Group(self.session, key=6)
        self.mockRequestsGET.assert_called_once_with(Session.ENDPOINT_URL + '/group', headers=mock.ANY)
        self.assertEqual(group.key, 6)
        self.assertEqual(group.name, 'Sales Users')
        self.assertEqual(group.gid, 4)
        self.assertEqual(list(group.users), [User(self.session, key=12, lazy_load=True), User(self.session, key=13, lazy_load=True)])

        # another load will not go to the server, but hit the cache
        group = Group(self.session, key=7)
        self.mockRequestsGET.assert_called_once_with(Session.ENDPOINT_URL + '/group', headers=mock.ANY)
        self.assertEqual(group.key, 7)
        self.assertEqual(group.name, 'Internal Users')
        self.assertEqual(group.gid, 8)
        self.assertEqual(list(group.users), [User(self.session, key=11, lazy_load=True), User(self.session, key=12, lazy_load=True), User(self.session, key=13, lazy_load=True)])
