import datetime
from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, ValidationError, ValueSerializer


class CustomField(Endpoint):

    ENDPOINT = '/customfield'

    LOAD_ALL = True

    class FIELD_TYPE(object):
        INPUT = 'input'
        SELECT = 'select'
        DATE = 'date'
        USER = 'user'
        COUNTRY = 'country'
        STATE = 'state'
        REGION = 'region'
        CONTACT = 'contact'
        COMPANY = 'company'
        CASE = 'case'
        OPPORTUNITY = 'opportunity'
        CURRENCY = 'currency'

        @classmethod
        def is_valid_field_type(cls, value):
            return value in (
                cls.INPUT,
                cls.SELECT,
                cls.DATE,
                cls.USER,
                cls.COUNTRY,
                cls.STATE,
                cls.REGION,
                cls.CONTACT,
                cls.COMPANY,
                cls.CASE,
                cls.OPPORTUNITY,
                cls.CURRENCY,
            )

    class FIELD_SCOPE(object):
        CONTACTS = 'customers'
        COMPANIES = 'companies'
        CASES = 'cases'
        OPPORTUNITIES = 'opportunities'

        @classmethod
        def is_valid_field_scope(cls, value):
            return isinstance(value, list) and value and all(v in (cls.CONTACTS, cls.COMPANIES, cls.CASES, cls.OPPORTUNITIES) for v in value)

    name = make_single_elem_property('name', string_types, '', 'The name of the custom field')
    full_name = make_single_elem_property('fullname', string_types, '', 'The full name of the custom field (where the custom field has an application specific prefix)')

    field_type = make_single_elem_property('elemType', string_types, '', 'The type of the custom field', validate_func=FIELD_TYPE.is_valid_field_type)
    field_scope = make_multi_elem_property('modelType', string_types, 'The scope of the custom field (what it is applicable to). A list of FIELD_SCOPE constants.', validate_func=FIELD_SCOPE.is_valid_field_scope)
    # TODO: app = ''

    is_multi_value = make_single_elem_property('multiple', bool, '', 'Specifies if this custom field allows multiple values or just a single value')

    allowed_values = make_multi_elem_property('values', string_types, 'The list of values allowed. Only populated for custom fields of type select.')

    def validate(self):
        if not self.name:
            raise ValidationError("The custom field needs a name.")
        field_type = self.field_type
        if not field_type:
            raise ValidationError("The custom field needs a field_type.")
        if field_type == self.FIELD_TYPE.SELECT and not self.allowed_values:
            raise ValidationError("A select custom field needs to specify the allowed_values property.")
        if not self.field_scope:
            raise ValidationError("The custom field needs a field_scope.")


class CustomFieldValue(ValueSerializer):

    def __init__(self, content=None, custom_field=None, custom_field_value=None, session=None):
        if content:
            assert custom_field is None and custom_field_value is None and isinstance(session, Session)
            keys = list(content)
            assert len(keys) == 1, "Invalid CustomFieldValue content: %s" % (content,)
            key = keys[0]
            assert isinstance(key, int)
            custom_field = CustomField(session, key=key, lazy_load=True)
            custom_field_value = content[key]
        else:
            assert custom_field is not None and custom_field_value is not None and session is None
        self._custom_field = custom_field
        self._custom_field_value = self._validate_value(custom_field_value)

    @property
    def custom_field(self):
        return self._custom_field

    def _get_cf_value(self):
        return self._custom_field_value

    def _set_cf_value(self, value):
        self._custom_field_value = self._validate_value(value)

    custom_field_value = property(_get_cf_value, _set_cf_value, None, "The value of the custom field")

    def _get_expected_value_types(self):
        from .contact import Contact
        from .company import Company
        from .case import Case
        from .opportunity import Opportunity
        from .user import User
        return {
            CustomField.FIELD_TYPE.INPUT: string_types,
            CustomField.FIELD_TYPE.SELECT: string_types,
            CustomField.FIELD_TYPE.DATE: (datetime.date, string_types),
            CustomField.FIELD_TYPE.USER: User,
            CustomField.FIELD_TYPE.COUNTRY: string_types,
            CustomField.FIELD_TYPE.STATE: string_types,
            CustomField.FIELD_TYPE.REGION: string_types,
            CustomField.FIELD_TYPE.CONTACT: Contact,
            CustomField.FIELD_TYPE.COMPANY: Company,
            CustomField.FIELD_TYPE.CASE: Case,
            CustomField.FIELD_TYPE.OPPORTUNITY: Opportunity,
            CustomField.FIELD_TYPE.CURRENCY: string_types,
        }

    def _check_expected_single_value_type(self, value):
        expected_types = self._get_expected_value_types()[self._custom_field.field_type]
        if not isinstance(value, expected_types):
            raise ValidationError("Incorrect value of type '%s'. Expected type(s): '%s'" % (type(value), expected_types))

    def _check_expected_type(self, value):
        if self._custom_field.is_multi_value:
            if not isinstance(value, (list, tuple)):
                raise ValidationError("Incorrect value for a multiple values custom field. Expected a list or a tuple.")
            for val in value:
                self._check_expected_single_value_type(val)
        else:
            self._check_expected_single_value_type(value)

    def _validate_value(self, value):
        """Validates a value when set"""
        self._check_expected_type(value)
        field_type = self._custom_field.field_type
        if field_type == CustomField.FIELD_TYPE.SELECT:
            def _validate_select_value(v):
                if v not in self._custom_field.allowed_values:
                    raise ValidationError("Incorrect value '%s' for a SELECT custom field. Allowed values: %s" % (v, ', '.join(self._custom_field.allowed_values)))
            if self._custom_field.is_multi_value:
                for val in value:
                    _validate_select_value(val)
            else:
                _validate_select_value(value)
        elif field_type == CustomField.FIELD_TYPE.DATE:
            def _transform_date_value(v):
                if isinstance(v, string_types):
                    try:
                        dt = datetime.datetime.strptime(v, '%Y-%m-%d')
                    except ValueError:
                        raise ValidationError("Incorrect value '%s' for a DATE custom field. Expected a YYYY-MM-DD formatted string or a datetime.date" % (v,))
                    v = dt.strftime('%Y-%m-%d')
                return v
            if self._custom_field.is_multi_value:
                value = [_transform_date_value(v) for v in value]
            else:
                value = _transform_date_value(value)
        return value

    def _transform_single_value(self, value):
        if Session.is_registered_endpoint(type(value)):
            value = '%s' % (value.key,)
        elif isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        return value

    def _transform_value(self):
        if self._custom_field.is_multi_value:
            return [self._transform_single_value(v) for v in self._custom_field_value]
        return self._transform_single_value(self._custom_field_value)

    def serialize(self):
        return {self._custom_field.key: self._transform_value()}

    def __eq__(self, other):
        return self._custom_field.key == other._custom_field.key and self._transform_value() == other._transform_value()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s' % (self.serialize(),)


class CustomFieldValueCollection(ValueSerializer):
    def __init__(self, content=None, session=None):
        assert isinstance(content, dict) and isinstance(session, Session)
        self._cf_by_id = {}
        # self._cf_by_name = {}
        self._content = content
        self.session = session
        items = tuple(content.items())
        for cf_id, cf_val in items:
            cf_id_int = int(cf_id)
            if cf_id_int != cf_id:
                del self._content[cf_id]
                self._content[cf_id_int] = cf_val
            cf = CustomField(session, key=cf_id_int, lazy_load=True)
            self._assert_custom_field_scope(cf)
            val = CustomFieldValue(
                custom_field=cf,
                custom_field_value=cf_val
            )
            self._cf_by_id[cf_id_int] = val

    def _assert_custom_field_scope(self, custom_field):
        cf_type = getattr(self, 'CUSTOM_FIELD_SCOPE', None)
        if cf_type is not None:
            assert cf_type in custom_field.field_scope

    def serialize(self):
        return self._content

    def __iter__(self):
        for cfv in self._cf_by_id.values():
            yield cfv

    def __getitem__(self, arg):
        if isinstance(arg, CustomField):
            assert arg.key is not None, "CustomField instance is not saved"
            return self._cf_by_id[arg.key]
        # elif isinstance(arg, string_types):
        #    return self._cf_by_name[arg]
        return self._cf_by_id[arg]

    def __setitem__(self, arg, value):
        if isinstance(arg, CustomField):
            assert arg.key is not None, "CustomField instance is not saved"
            key = arg.key
            self._assert_custom_field_scope(arg)
            val = CustomFieldValue(
                custom_field=arg,
                custom_field_value=value
            )
        else:
            key = arg
            cf = CustomField(self.session, key=arg, lazy_load=True)
            self._assert_custom_field_scope(cf)
            val = CustomFieldValue(
                custom_field=cf,
                custom_field_value=value
            )
        self._cf_by_id[key] = val
        self._content.update(val.serialize())

    def get(self, arg, default=None):
        try:
            return self[arg]
        except KeyError:
            return default


class ContactsCustomFieldValueCollection(CustomFieldValueCollection):
    CUSTOM_FIELD_SCOPE = CustomField.FIELD_SCOPE.CONTACTS


class CompaniesCustomFieldValueCollection(CustomFieldValueCollection):
    CUSTOM_FIELD_SCOPE = CustomField.FIELD_SCOPE.COMPANIES


class CasesCustomFieldValueCollection(CustomFieldValueCollection):
    CUSTOM_FIELD_SCOPE = CustomField.FIELD_SCOPE.CASES


class OpportunitiesCustomFieldValueCollection(CustomFieldValueCollection):
    CUSTOM_FIELD_SCOPE = CustomField.FIELD_SCOPE.OPPORTUNITIES


Session.register_endpoint(CustomField)
