from clevertimapi.session import Session
from clevertimapi.contact import Contact, PhoneNumber, SocialMediaId
from clevertimapi.company import Company
from clevertimapi.task import Task
from clevertimapi.opportunity import Opportunity
from clevertimapi.case import Case
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


class TestContact(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.contact1 = {
            'fn': 'Mike',
            'ln': 'Doodley',
            'title': 'Engineer',
            'is_company': False,
            'companyId': 999,
            'address': '199 Maverick Road',
            'city': 'London',
            'postcode': 'SW19 7BH',
            'region': 'US-FL',
            'country': 'US',
            'description': 'Mike is a great, likeable guy. He always returns my calls.',
            'email': ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com'],
            'website': ['http://www.google.com', 'http://www.mikedoodley.com'],
            'phones': [{'no': '07979463643', 'type': 'Work'}, {'no': '07979363643', 'type': 'Home'}, {'no': '07979163643', 'type': 'Mobile'}],
            'smids': [{'smid': 'mikesp40', 'type': 'Google+'}, {'smid': 'ciprianmiclaus', 'type': 'Github'}, {'smid': 'cippy', 'type': 'Skype'}],
            'cf': {'1': 'test', '2': 'cf_value2', '3': '2017-05-22', '4': 'US', '5': 'CA', '6': 'US-CA', '7': 'USD'},
            'tags': ['tag1', 'tag2', 'tag3'],
            'tasks': [1, 2],
            'opportunities': [100, 101, 211],
            'cases': [55, 57],
            'files': [22, 34],
            'lfiles': [120, 330, 454],
        }
        self.contact1_ret = deepcopy(self.contact1)
        self.contact1_ret.update({
            'id': 445,
            'lc': '2017-01-02T05:22:12Z',
            'cphoto': 'pic.jpg',
        })
        self.contact2 = {
            'id': 445,
            'fn': 'John',
            'ln': 'Rowdy',
            'title': 'CEO',
            'is_company': False,
            'companyId': 456,
            'address': '32 Bossy Lane',
            'city': 'Winchester',
            'postcode': 'WH7 8AB',
            'region': 'GB-WRL',
            'country': 'GB',
            'description': 'John is very bossy. He even lives on a bossy lane.',
            'email': ['john.rowdy@gmail.com', 'john.rowdy@yahoo.com'],
            'website': ['http://www.johnrowdy.com', 'http://www.yahoo.com'],
            'phones': [{'no': '+4407979463643', 'type': 'Fax'}, {'no': '+4407979363643', 'type': 'Pager'}, {'no': '+4407979163643', 'type': 'Work'}],
            'smids': [{'smid': 'dumbo33', 'type': 'YouTube'}, {'smid': 'miky22', 'type': 'Whatsapp'}],
            'cf': {'1': 'test2', '2': 'cf_value2', '3': '2017-05-22', '4': 'US', '5': 'CA', '6': 'US-CA', '7': 'USD'},
            'tags': ['othertag1', 'othertag2', 'othertag3'],
            'tasks': [3, 4, 2],
            'opportunities': [45, 101, 33],
            'cases': [55, 89],
            'files': [11, 23],
            'lfiles': [121, 331, 455],
            'lc': '2017-01-02T05:22:12Z',
            'cphoto': 'pic.jpg',
        }

    def _compare_against_contact1_ret(self, c):
        self.assertEqual(c.key, 445)
        self.assertEqual(c.first_name, 'Mike')
        self.assertEqual(c.last_name, 'Doodley')
        self.assertEqual(c.title, 'Engineer')
        self.assertEqual(c.address, '199 Maverick Road')
        self.assertEqual(c.city, 'London')
        self.assertEqual(c.postcode, 'SW19 7BH')
        self.assertEqual(c.region, 'US-FL')
        self.assertEqual(c.country, 'US')
        self.assertEqual(c.description, 'Mike is a great, likeable guy. He always returns my calls.')
        self.assertEqual(c.emails, ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com'])
        self.assertEqual(c.websites, ['http://www.google.com', 'http://www.mikedoodley.com'])
        self.assertEqual(list(c.phone_numbers), [
            PhoneNumber(phone_number='07979463643', phone_type='Work'),
            PhoneNumber(phone_number='07979363643', phone_type='Home'),
            PhoneNumber(phone_number='07979163643', phone_type='Mobile'),
        ])
        self.assertEqual(list(c.social_media_ids), [
            SocialMediaId(social_media_id='mikesp40', social_media_type='Google+'),
            SocialMediaId(social_media_id='ciprianmiclaus', social_media_type='Github'),
            SocialMediaId(social_media_id='cippy', social_media_type='Skype'),
        ])

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

        self.assertIsInstance(c.company, Company)
        self.assertEqual(c.company.key, 999)

        self.assertTrue(all(isinstance(t, Task) for t in c.tasks))
        self.assertEqual([t.key for t in c.tasks], [1, 2])
        self.assertTrue(all(isinstance(t, Opportunity) for t in c.opportunities))
        self.assertEqual([t.key for t in c.opportunities], [100, 101, 211])
        self.assertTrue(all(isinstance(t, Case) for t in c.cases))
        self.assertEqual([t.key for t in c.cases], [55, 57])
        self.assertEqual([t.key for t in c.files], [22, 34])
        self.assertEqual([t.key for t in c.linked_files], [120, 330, 454])

        self.assertEqual(c.last_contacted, '2017-01-02T05:22:12Z')
        self.assertEqual(c.contact_photo, 'https://www.clevertim.com/getcphoto/445/pic.jpg')

    @mock.patch('requests.get')
    def test_load_contact(self, mockRequestsGET):
        setup_requests_call_mock(mockRequestsGET, {
            '/contact/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.contact1_ret
                    ]
                })
            )
        })
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.CONTACTS)

        c = Contact(self.session, key=445)
        self.assertFalse(c.is_new())
        self._compare_against_contact1_ret(c)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_add_new_contact(self, mockRequestsGET, mockRequestsPOST):
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.CONTACTS)
        setup_requests_call_mock(mockRequestsPOST, {
            '/contact': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.contact1_ret
                    ]
                })
            )
        })

        c = Contact(self.session)
        c.first_name = 'Mike'
        c.last_name = 'Doodley'
        c.title = 'Engineer'
        c.address = '199 Maverick Road'
        c.city = 'London'
        c.postcode = 'SW19 7BH'
        c.region = 'US-FL'
        c.country = 'US'
        c.description = 'Mike is a great, likeable guy. He always returns my calls.'
        c.emails = ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com']
        c.websites = ['http://www.google.com', 'http://www.mikedoodley.com']
        c.phone_numbers = [
            PhoneNumber(phone_number='07979463643', phone_type='Work'),
            PhoneNumber(phone_number='07979363643', phone_type='Home'),
            PhoneNumber(phone_number='07979163643', phone_type='Mobile'),
        ]
        c.social_media_ids = [
            SocialMediaId(social_media_id='mikesp40', social_media_type='Google+'),
            SocialMediaId(social_media_id='ciprianmiclaus', social_media_type='Github'),
            SocialMediaId(social_media_id='cippy', social_media_type='Skype'),
        ]
        c.custom_field_values[1] = "test"
        c.custom_field_values[2] = "cf_value2"
        c.custom_field_values[3] = datetime.date(2017, 5, 22)
        c.custom_field_values[CustomField(self.session, key=4, lazy_load=True)] = "US"
        c.custom_field_values[5] = "CA"
        c.custom_field_values[6] = "US-CA"
        c.custom_field_values[7] = "USD"

        c.tags = ['tag1', 'tag2', 'tag3']

        c.company = Company(self.session, key=999, lazy_load=True)

        c.tasks = [Task(self.session, key=1, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.opportunities = [Opportunity(self.session, key=100, lazy_load=True), Opportunity(self.session, key=101, lazy_load=True), Opportunity(self.session, key=211, lazy_load=True)]
        c.cases = [Case(self.session, key=55, lazy_load=True), Case(self.session, key=57, lazy_load=True)]
        c.files = [File(self.session, key=22, lazy_load=True), File(self.session, key=34, lazy_load=True)]
        c.linked_files = [LinkedFile(self.session, key=120, lazy_load=True), LinkedFile(self.session, key=330, lazy_load=True), LinkedFile(self.session, key=454, lazy_load=True)]

        self.assertTrue(c.is_new())
        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPOST.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Contact.ENDPOINT)
        self.assertEqual(data, self.contact1)

        self._compare_against_contact1_ret(c)

    @mock.patch('requests.put')
    @mock.patch('requests.get')
    def test_edit_existing_contact(self, mockRequestsGET, mockRequestsPUT):
        setup_requests_call_mock(mockRequestsGET, {
            '/contact/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.contact1_ret
                    ]
                })
            )
        })
        set_up_GET_custom_fields(mockRequestsGET, CustomField.FIELD_SCOPE.CONTACTS)
        setup_requests_call_mock(mockRequestsPUT, {
            '/contact/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        {
                            'id': 445,
                            'lc': '2017-01-02T05:22:12Z',
                        }
                    ]
                })
            )
        })

        c = Contact(self.session, key=445)
        c.first_name = 'John'
        c.last_name = 'Rowdy'
        c.title = 'CEO'
        c.address = '32 Bossy Lane'
        c.city = 'Winchester'
        c.postcode = 'WH7 8AB'
        c.region = 'GB-WRL'
        c.country = 'GB'
        c.description = 'John is very bossy. He even lives on a bossy lane.'
        c.emails = ['john.rowdy@gmail.com', 'john.rowdy@yahoo.com']
        c.websites = ['http://www.johnrowdy.com', 'http://www.yahoo.com']
        c.phone_numbers = [
            PhoneNumber(phone_number='+4407979463643', phone_type='Fax'),
            PhoneNumber(phone_number='+4407979363643', phone_type='Pager'),
            PhoneNumber(phone_number='+4407979163643', phone_type='Work'),
        ]
        c.social_media_ids = [
            SocialMediaId(social_media_id='dumbo33', social_media_type='YouTube'),
            SocialMediaId(social_media_id='miky22', social_media_type='Whatsapp'),
        ]
        c.custom_field_values[1] = "test2"
        c.tags = ['othertag1', 'othertag2', 'othertag3']

        c.company = Company(self.session, key=456, lazy_load=True)

        c.tasks = [Task(self.session, key=3, lazy_load=True), Task(self.session, key=4, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.opportunities = [Opportunity(self.session, key=45, lazy_load=True), Opportunity(self.session, key=101, lazy_load=True), Opportunity(self.session, key=33, lazy_load=True)]
        c.cases = [Case(self.session, key=55, lazy_load=True), Case(self.session, key=89, lazy_load=True)]
        c.files = [File(self.session, key=11, lazy_load=True), File(self.session, key=23, lazy_load=True)]
        c.linked_files = [LinkedFile(self.session, key=121, lazy_load=True), LinkedFile(self.session, key=331, lazy_load=True), LinkedFile(self.session, key=455, lazy_load=True)]

        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPUT.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Contact.ENDPOINT + '/445')
        self.assertEqual(data, self.contact2)

        self.assertEqual(c.contact_photo, 'https://www.clevertim.com/getcphoto/445/pic.jpg')
