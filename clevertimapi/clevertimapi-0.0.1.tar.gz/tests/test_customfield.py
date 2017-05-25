import datetime
from clevertimapi.session import Session
from clevertimapi.customfield import CustomField, CustomFieldValue
from clevertimapi.user import User
from clevertimapi.endpoint import ValidationError
import json
from mock_utils import setup_requests_call_mock, set_up_GET_custom_fields
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestCustomFieldValidation(unittest.TestCase):

    def setUp(self):
        self.session = Session('APIKEY')
        self.mockRequestsGET = mock.patch('requests.get').start()
        set_up_GET_custom_fields(self.mockRequestsGET, CustomField.FIELD_SCOPE.CONTACTS)

    def tearDown(self):
        mock.patch.stopall()

    def test_invalid_field_type_raises_on_set_lazy(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        with self.assertRaises(ValidationError):
            cf.field_type = 'UNSUPPORTED'
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_invalid_field_type_raises_on_set_unlazy(self):
        cf = CustomField(self.session, key=1, lazy_load=False)
        with self.assertRaises(ValidationError):
            cf.field_type = 'UNSUPPORTED'
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_invalid_field_type_raises_on_set_lazy_not_saved(self):
        cf = CustomField(self.session, lazy_load=True)
        with self.assertRaises(ValidationError):
            cf.field_type = 'UNSUPPORTED'
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_invalid_field_type_raises_on_set_unlazy_not_saved(self):
        cf = CustomField(self.session, lazy_load=False)
        with self.assertRaises(ValidationError):
            cf.field_type = 'UNSUPPORTED'
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_invalid_field_scope_raises_on_set_lazy(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        with self.assertRaises(ValidationError):
            cf.field_scope = ['UNSUPPORTED']
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_invalid_field_scope_raises_on_set_unlazy(self):
        cf = CustomField(self.session, key=1, lazy_load=False)
        with self.assertRaises(ValidationError):
            cf.field_scope = ['UNSUPPORTED']
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_invalid_field_scope_raises_on_set_lazy_not_saved(self):
        cf = CustomField(self.session, lazy_load=True)
        with self.assertRaises(ValidationError):
            cf.field_scope = ['UNSUPPORTED']
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_invalid_field_scope_raises_on_set_unlazy_not_saved(self):
        cf = CustomField(self.session, lazy_load=False)
        with self.assertRaises(ValidationError):
            cf.field_scope = ['UNSUPPORTED']
        self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_custom_field_with_no_name_raises_on_save(self):
        cf = CustomField(self.session)
        cf.field_type = CustomField.FIELD_TYPE.INPUT
        cf.field_scope = [CustomField.FIELD_SCOPE.CONTACTS]
        with self.assertRaises(ValidationError) as verr:
            cf.save()
        self.assertEqual(str(verr.exception), "The custom field needs a name.")

    def test_custom_field_with_no_field_scope_raises_on_save(self):
        cf = CustomField(self.session)
        cf.name = 'Custom Field'
        cf.field_type = CustomField.FIELD_TYPE.INPUT
        with self.assertRaises(ValidationError) as verr:
            cf.save()
        self.assertEqual(str(verr.exception), "The custom field needs a field_scope.")

    def test_custom_field_with_no_field_type_raises_on_save(self):
        cf = CustomField(self.session)
        cf.name = 'Custom Field'
        cf.field_scope = [CustomField.FIELD_SCOPE.CONTACTS]
        with self.assertRaises(ValidationError) as verr:
            cf.save()
        self.assertEqual(str(verr.exception), "The custom field needs a field_type.")

    def test_select_field_with_no_allowed_values_raises_on_save(self):
        cf = CustomField(self.session)
        cf.name = 'Custom Field'
        cf.field_type = CustomField.FIELD_TYPE.SELECT
        cf.field_scope = [CustomField.FIELD_SCOPE.CONTACTS]
        with self.assertRaises(ValidationError) as verr:
            cf.save()
        self.assertEqual(str(verr.exception), "A select custom field needs to specify the allowed_values property.")

    @mock.patch('requests.post')
    def test_select_field_validation_successful(self, mockRequestsPOST):
        setup_requests_call_mock(mockRequestsPOST, {
            '/customfield': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 1022
                    }]
                })
            )}
        )

        cf = CustomField(self.session)
        cf.name = 'Custom Field'
        cf.field_type = CustomField.FIELD_TYPE.SELECT
        cf.field_scope = [CustomField.FIELD_SCOPE.CONTACTS]
        cf.allowed_values = ['cf_val1', 'cf_val2', 'cf_val3']
        cf.save()
        self.assertEqual(mockRequestsPOST.call_count, 1)
        self.assertEqual(cf.key, 1022)


class TestCustomFieldValue(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')
        self.mockRequestsGET = mock.patch('requests.get').start()
        set_up_GET_custom_fields(self.mockRequestsGET, CustomField.FIELD_SCOPE.CONTACTS)

    def tearDown(self):
        mock.patch.stopall()

    def test_instantiate_serialize_compare(self):
        cfv = CustomFieldValue(content={1: 'test'}, session=self.session)
        ret = cfv.serialize()
        self.assertEqual(ret, {1: 'test'})

        cf = CustomField(self.session, key=1, lazy_load=True)
        cfv2 = CustomFieldValue(custom_field=cf, custom_field_value='test')
        cfv3 = CustomFieldValue(custom_field=cf, custom_field_value='test2')
        ret = cfv2.serialize()
        self.assertEqual(ret, {1: 'test'})
        ret = cfv3.serialize()
        self.assertEqual(ret, {1: 'test2'})

        self.assertEqual(cfv, cfv2)
        self.assertNotEqual(cfv, cfv3)

        self.assertEqual(cfv3.custom_field, cf)
        self.assertEqual(cfv3.custom_field_value, 'test2')

    def test_custom_field_property_is_readonly(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='test')
        with self.assertRaises(AttributeError):
            cfv.custom_field = CustomField(self.session, key=2, lazy_load=True)

    def test_custom_field_value_property_can_be_set(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='test')
        ret = cfv.serialize()
        self.assertEqual(ret, {1: 'test'})
        cfv.custom_field_value = 'test2'
        ret = cfv.serialize()
        self.assertEqual(ret, {1: 'test2'})
        self.assertEqual(repr(cfv), "{1: 'test2'}")

    def test_single_input_custom_field_fails_when_set_with_wrong_type(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.INPUT)
        with self.assertRaises(ValidationError):
            cfv = CustomFieldValue(custom_field=cf, custom_field_value=100)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='test')
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = {'invalid': 'value'}

    def test_single_select_custom_field_fails_when_set_with_wrong_type(self):
        cf = CustomField(self.session, key=2, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.SELECT)
        with self.assertRaises(ValidationError):
            cfv = CustomFieldValue(custom_field=cf, custom_field_value=400)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='cf_value3')
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = {'invalid': 'value'}

    def test_single_date_custom_field_fails_when_set_with_wrong_type(self):
        cf = CustomField(self.session, key=3, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        with self.assertRaises(ValidationError):
            cfv = CustomFieldValue(custom_field=cf, custom_field_value=400)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=datetime.date(2017, 3, 11))
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = {'invalid': 'value'}

    def test_single_custom_field_fails_when_set_to_list(self):
        cf = CustomField(self.session, key=1, lazy_load=True)
        self.assertFalse(cf.is_multi_value)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='test')
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = ['test1', 'test2']

    def test_multiple_custom_field_fails_when_set_to_single_value(self):
        cf = CustomField(self.session, key=13, lazy_load=True)
        self.assertTrue(cf.is_multi_value)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=['test', 'test2'])
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = 'test3'

    def test_single_select_field_cannot_be_instantiated_with_incorrect_value(self):
        cf = CustomField(self.session, key=2, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.SELECT)
        with self.assertRaises(ValidationError):
            CustomFieldValue(custom_field=cf, custom_field_value='test')

    def test_single_select_field_cannot_be_instantiated_with_incorrect_value2(self):
        cf = CustomField(self.session, key=2, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.SELECT)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='cf_value2')
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = 'test'

    def test_multiple_select_field_cannot_be_instantiated_with_incorrect_value(self):
        cf = CustomField(self.session, key=14, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.SELECT)
        with self.assertRaises(ValidationError):
            CustomFieldValue(custom_field=cf, custom_field_value=['test'])

    def test_multiple_select_field_cannot_be_instantiated_with_incorrect_value2(self):
        cf = CustomField(self.session, key=14, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.SELECT)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=['cf_value1', 'cf_value2'])
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = ['test']

    def test_single_date_field_cannot_be_instantiated_with_incorrect_value(self):
        cf = CustomField(self.session, key=3, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        with self.assertRaises(ValidationError):
            CustomFieldValue(custom_field=cf, custom_field_value='test')

    def test_single_date_field_cannot_be_instantiated_with_incorrect_value2(self):
        cf = CustomField(self.session, key=3, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='2017-02-20')
        cfv2 = CustomFieldValue(custom_field=cf, custom_field_value=datetime.date(2017, 2, 20))
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = 'test'
        with self.assertRaises(ValidationError):
            cfv2.custom_field_value = 'test'
        self.assertEqual(cfv, cfv2)

    def test_multiple_date_field_cannot_be_instantiated_with_incorrect_value(self):
        cf = CustomField(self.session, key=15, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        with self.assertRaises(ValidationError):
            CustomFieldValue(custom_field=cf, custom_field_value=['test'])

    def test_multiple_date_field_cannot_be_instantiated_with_incorrect_value2(self):
        cf = CustomField(self.session, key=15, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=['2017-02-20', datetime.date(2017, 2, 21)])
        cfv2 = CustomFieldValue(custom_field=cf, custom_field_value=[datetime.date(2017, 2, 20), '2017-02-21'])
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = ['test']
        with self.assertRaises(ValidationError):
            cfv2.custom_field_value = [{}]
        self.assertEqual(cfv, cfv2)

    def test_date_field_serializes_correctly(self):
        cf = CustomField(self.session, key=3, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.DATE)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value='2017-02-20')
        ret = cfv.serialize()
        self.assertEqual(ret, {3: '2017-02-20'})
        cfv2 = CustomFieldValue(custom_field=cf, custom_field_value=datetime.date(2017, 2, 20))
        ret = cfv2.serialize()
        self.assertEqual(ret, {3: '2017-02-20'})
        self.assertEqual(cfv, cfv2)

    def test_user_field_cannot_be_instantiated_with_incorrect_value(self):
        cf = CustomField(self.session, key=8, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.USER)
        with self.assertRaises(ValidationError):
            CustomFieldValue(custom_field=cf, custom_field_value='test')

    def test_user_field_cannot_be_instantiated_with_incorrect_value2(self):
        cf = CustomField(self.session, key=8, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.USER)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=User(self.session, key=8989, lazy_load=True))
        with self.assertRaises(ValidationError):
            cfv.custom_field_value = 'test'

    def test_user_field_serializes_correctly(self):
        cf = CustomField(self.session, key=8, lazy_load=True)
        self.assertEqual(cf.field_type, CustomField.FIELD_TYPE.USER)
        cfv = CustomFieldValue(custom_field=cf, custom_field_value=User(self.session, key=9987, lazy_load=True))
        ret = cfv.serialize()
        self.assertEqual(ret, {8: '9987'})
        cfv2 = CustomFieldValue(custom_field=cf, custom_field_value=User(self.session, key=9987, lazy_load=True))
        ret = cfv.serialize()
        self.assertEqual(ret, {8: '9987'})
        self.assertEqual(cfv, cfv2)
