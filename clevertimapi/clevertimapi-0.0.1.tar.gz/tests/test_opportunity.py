from clevertimapi.session import Session
from clevertimapi.opportunity import Opportunity
from clevertimapi.task import Task
from clevertimapi.user import User
from clevertimapi.customfield import CustomField, CustomFieldValue
from clevertimapi.file import File, LinkedFile
from copy import deepcopy
import datetime
from mock_utils import setup_requests_call_mock, set_up_GET_custom_fields
import json
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestOpportunity(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.opp1 = {
            'name': 'Opportunity 1',
            'description': 'Clevertim is a great company. They do software.',
            # 'cust': 1,
            'leadUser': 2,
            'currency': 'EUR',
            'value': '1000.50',
            'status': 'Won',
            'cf': {'1': 'test', '2': 'cf_value2', '3': '2017-05-22', '4': 'US', '5': 'CA', '6': 'US-CA', '7': 'USD'},
            'tags': ['tag1', 'tag2', 'tag3'],
            'tasks': [1, 2],
            'files': [22, 34],
            'lfiles': [120, 330, 454],
        }
        self.opp1_ret = deepcopy(self.opp1)
        self.opp1_ret.update({
            'id': 445,
        })
        self.opp2 = {
            'id': 445,
            'name': 'Opportunity 2',
            'description': 'Some Ltd. is fantastic. Its customer support is unlike anything out there.',
            # 'cust': 2,
            'leadUser': 3,
            'currency': 'GBP',
            'value': '652.75',
            'status': 'Lost',
            'cf': {'1': 'test2', '2': 'cf_value2', '3': '2017-05-22', '4': 'US', '5': 'CA', '6': 'US-CA', '7': 'USD'},
            'tags': ['othertag1', 'othertag2', 'othertag3'],
            'tasks': [3, 4, 2],
            'files': [11, 23],
            'lfiles': [121, 331, 455],
        }

    def _compare_against_opp1_ret(self, c):
        self.assertEqual(c.key, 445)
        self.assertEqual(c.name, 'Opportunity 1')
        self.assertEqual(c.description, 'Clevertim is a great company. They do software.')

        self.assertEqual(c.currency, 'EUR')
        self.assertEqual(c.value, '1000.50')
        self.assertEqual(c.status, 'Won')

        values = [
            CustomFieldValue(custom_field=CustomField(self.session, key=1, lazy_load=True), custom_field_value="test"),
            CustomFieldValue(custom_field=CustomField(self.session, key=2, lazy_load=True), custom_field_value="cf_value2"),
            CustomFieldValue(custom_field=CustomField(self.session, key=3, lazy_load=True), custom_field_value="2017-05-22"),
            CustomFieldValue(custom_field=CustomField(self.session, key=4, lazy_load=True), custom_field_value="US"),
            CustomFieldValue(custom_field=CustomField(self.session, key=5, lazy_load=True), custom_field_value="CA"),
            CustomFieldValue(custom_field=CustomField(self.session, key=6, lazy_load=True), custom_field_value="US-CA"),
            CustomFieldValue(custom_field=CustomField(self.session, key=7, lazy_load=True), custom_field_value="USD"),
        ]
        self.assertEqual(sorted(c.custom_field_values, key=lambda cfv: cfv.custom_field.key), values)
        for key in range(1, 8):
            cf = CustomField(self.session, key=key, lazy_load=True)
            self.assertEqual(c.custom_field_values[cf], values[key - 1])

        self.assertEqual(c.custom_field_values.get(7), values[6])
        self.assertEqual(c.custom_field_values.get(CustomField(self.session, key=7, lazy_load=True)), values[6])
        self.assertIsNone(c.custom_field_values.get(12345))
        self.assertIsNone(c.custom_field_values.get(CustomField(self.session, key=12345, lazy_load=True)))

        self.assertEqual(c.tags, ['tag1', 'tag2', 'tag3'])

        self.assertIsInstance(c.lead_user, User)
        self.assertEqual(c.lead_user.key, 2)

        self.assertTrue(all(isinstance(t, Task) for t in c.tasks))
        self.assertEqual([t.key for t in c.tasks], [1, 2])
        self.assertEqual([t.key for t in c.files], [22, 34])
        self.assertEqual([t.key for t in c.linked_files], [120, 330, 454])

    @mock.patch('requests.get')
    def test_load_opportunity(self, mockRequestsGET):
        setup_requests_call_mock(mockRequestsGET, {
            '/opportunity/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.opp1_ret
                    ]
                })
            )
        })
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.OPPORTUNITIES)

        c = Opportunity(self.session, key=445)
        self.assertFalse(c.is_new())
        self._compare_against_opp1_ret(c)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_add_new_opportunity(self, mockRequestsGET, mockRequestsPOST):
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.OPPORTUNITIES)
        setup_requests_call_mock(mockRequestsPOST, {
            '/opportunity': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.opp1_ret
                    ]
                })
            )
        })

        c = Opportunity(self.session)
        c.name = 'Opportunity 1'
        c.description = 'Clevertim is a great company. They do software.'
        c.currency = 'EUR'
        c.value = '1000.50'
        c.status = 'Won'
        c.custom_field_values[1] = "test"
        c.custom_field_values[2] = "cf_value2"
        c.custom_field_values[3] = datetime.date(2017, 5, 22)
        c.custom_field_values[CustomField(self.session, key=4, lazy_load=True)] = "US"
        c.custom_field_values[5] = "CA"
        c.custom_field_values[6] = "US-CA"
        c.custom_field_values[7] = "USD"

        c.tags = ['tag1', 'tag2', 'tag3']

        c.lead_user = User(self.session, key=2, lazy_load=True)

        c.tasks = [Task(self.session, key=1, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.files = [File(self.session, key=22, lazy_load=True), File(self.session, key=34, lazy_load=True)]
        c.linked_files = [LinkedFile(self.session, key=120, lazy_load=True), LinkedFile(self.session, key=330, lazy_load=True), LinkedFile(self.session, key=454, lazy_load=True)]

        self.assertTrue(c.is_new())
        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPOST.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Opportunity.ENDPOINT)
        self.assertEqual(data, self.opp1)

        self._compare_against_opp1_ret(c)

    @mock.patch('requests.put')
    @mock.patch('requests.get')
    def test_edit_existing_opportunity(self, mockRequestsGET, mockRequestsPUT):
        setup_requests_call_mock(mockRequestsGET, {
            '/opportunity/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.opp1_ret
                    ]
                })
            )
        })
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.OPPORTUNITIES)
        setup_requests_call_mock(mockRequestsPUT, {
            '/opportunity/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        {
                            'id': 445,
                        }
                    ]
                })
            )
        })

        c = Opportunity(self.session, key=445)
        c.name = 'Opportunity 2'
        c.description = 'Some Ltd. is fantastic. Its customer support is unlike anything out there.'
        c.currency = 'GBP'
        c.value = '652.75'
        c.status = 'Lost'

        c.lead_user = User(self.session, key=3, lazy_load=True)

        c.custom_field_values[1] = "test2"
        c.tags = ['othertag1', 'othertag2', 'othertag3']

        c.tasks = [Task(self.session, key=3, lazy_load=True), Task(self.session, key=4, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.files = [File(self.session, key=11, lazy_load=True), File(self.session, key=23, lazy_load=True)]
        c.linked_files = [LinkedFile(self.session, key=121, lazy_load=True), LinkedFile(self.session, key=331, lazy_load=True), LinkedFile(self.session, key=455, lazy_load=True)]

        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPUT.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Opportunity.ENDPOINT + '/445')
        self.assertEqual(data, self.opp2)
