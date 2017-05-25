import datetime
import json
from copy import deepcopy
from clevertimapi.session import Session
from clevertimapi.task import Task
from clevertimapi.contact import Contact
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


class TestTask(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.task1 = {
            'atype': 'Email',
            'atypet': 'Email',
            'name': 'Clean up the dishes',
            'userId': 5,
            'aUserId': 7,
            'location': 'Bromley',
            'cust': 101,
            'case': 333,
            'opp': 123,
            'startDate': {'y': 2017, 'mo': 5, 'd': 10, 'h': 9, 'mi': 0},
            'endDate': {'y': 2017, 'mo': 5, 'd': 10, 'h': 10, 'mi': 0},
            # 'rec':
            'is_completed': False,
            'is_deleted': False,
            'ao': '2017-01-02T05:22:12Z',
            'lm': '2017-01-02T08:22:12Z',
            'is_private': False,
            'gid': 0,
            'puser': None,
            'comments': [4, 9, 12],
        }
        self.task1_ret = deepcopy(self.task1)
        self.task1_ret.update({
            'id': 445,
        })
        self.task2 = {
            'atype': 'Call',
            'atypet': 'Email',
            'name': 'Clean up the dishes',
            'userId': 5,
            'aUserId': 7,
            'location': 'Bromley',
            'cust': 101,
            'case': 333,
            'opp': 123,
            'startDate': {'y': 2017, 'mo': 5, 'd': 10, 'h': 9, 'mi': 0},
            'endDate': {'y': 2017, 'mo': 5, 'd': 10, 'h': 10, 'mi': 0},
            'rec': 'N',
            'is_completed': False,
            'is_deleted': False,
            'ao': '2017-01-02T05:22:12Z',
            'lm': '2017-01-02T08:22:12Z',
            'is_private': False,
            'gid': 0,
            'puser': None,
            'comments': [4, 9, 12],
        }

    def _compare_against_task1_ret(self, c):
        self.assertEqual(c.key, 445)
        self.assertEqual(c.name, 'Clean up the dishes')
        self.assertEqual(c.task_type, 'Email')
        self.assertEqual(c.location, 'Bromley')
        self.assertEqual(c.who, Contact(self.session, key=101))
        self.assertEqual(c.start_date, datetime.date(2017, 5, 10))
        self.assertEqual(c.start_time, datetime.time(9, 0))

    def test_dates(self):
        t = Task(self.session)
        t.start_date = datetime.date(2017, 6, 9)
        t.start_time = datetime.time(11, 30)
        t.end_date = datetime.date(2017, 6, 10)
        t.end_time = datetime.time(12, 30)
        self.assertEqual(t.get_content(), {
            'startDate': {'y': 2017, 'mo': 6, 'd': 9, 'h': 11, 'mi': 30},
            'endDate': {'y': 2017, 'mo': 6, 'd': 10, 'h': 12, 'mi': 30},
        })

    @mock.patch('requests.get')
    def test_load_task(self, mockRequestsGET):
        setup_requests_call_mock(mockRequestsGET, {
            '/task/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.task1_ret
                    ]
                })
            ),
            '/contact/101': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 101,
                        'fn': 'Miky Gory',
                    }]
                })
            )
        })

        c = Task(self.session, key=445)
        self.assertFalse(c.is_new())
        self._compare_against_task1_ret(c)
