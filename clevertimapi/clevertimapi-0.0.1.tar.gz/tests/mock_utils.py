import json
from clevertimapi.customfield import CustomField
from clevertimapi.session import Session
try:
    import unittest.mock as mock
except ImportError:
    import mock


def setup_requests_call_mock(requestsMockObj, config):
    prev_side_effect = requestsMockObj.side_effect

    def requests_call(*args, **kwargs):
        url = args[0]
        for endpoint, (status_code, response_text) in config.items():
            if url == Session.build_url(Session.ENDPOINT_URL, endpoint):
                mock_response = mock.Mock()
                mock_response.status_code = status_code
                mock_response.text = response_text
                return mock_response
        if prev_side_effect:
            return prev_side_effect(*args, **kwargs)
        else:
            raise LookupError("Cannot find a mock for requests.get for url:%s" % (url,))

    requestsMockObj.side_effect = requests_call


def generate_custom_field_info(key, name, field_type, field_scope, multiple, values):
    ret = {
        'id': key,
        'name': name,
        'fullname': name,
        'elemType': field_type,
        'modelType': [field_scope],
        'multiple': multiple,
        'app': None
    }
    if values is not None:
        ret['values'] = values
    return ret


def get_custom_fields_fixtures(field_scope):
    single_fixtures = [
        (1, 'Input Custom Field', CustomField.FIELD_TYPE.INPUT, field_scope, False, None),
        (2, 'Select Custom Field', CustomField.FIELD_TYPE.SELECT, field_scope, False, ['cf_value1', 'cf_value2', 'cf_value3', 'cf_value4']),
        (3, 'Date Custom Field', CustomField.FIELD_TYPE.DATE, field_scope, False, None),
        (4, 'Country Custom Field', CustomField.FIELD_TYPE.COUNTRY, field_scope, False, None),
        (5, 'State Custom Field', CustomField.FIELD_TYPE.STATE, field_scope, False, None),
        (6, 'Region Custom Field', CustomField.FIELD_TYPE.REGION, field_scope, False, None),
        (7, 'Currency Custom Field', CustomField.FIELD_TYPE.CURRENCY, field_scope, False, None),
        (8, 'User Custom Field', CustomField.FIELD_TYPE.USER, field_scope, False, None),
        (9, 'Contact Custom Field', CustomField.FIELD_TYPE.CONTACT, field_scope, False, None),
        (10, 'Company Custom Field', CustomField.FIELD_TYPE.COMPANY, field_scope, False, None),
        (11, 'Case Custom Field', CustomField.FIELD_TYPE.CASE, field_scope, False, None),
        (12, 'Opportunity Custom Field', CustomField.FIELD_TYPE.OPPORTUNITY, field_scope, False, None),
    ]
    multiple_fixtures = [
        (_id + len(single_fixtures), _name, _type, _scope, True, _value) for (_id, _name, _type, _scope, _, _value) in single_fixtures
    ]
    all_fixtures = single_fixtures + multiple_fixtures
    return all_fixtures


def set_up_GET_custom_fields(requestsGETMockObj, field_scope):
    all_fixtures = get_custom_fields_fixtures(field_scope)
    config = {}
    content = []
    for fixture in all_fixtures:
        content.append(generate_custom_field_info(*fixture))
    config['/customfield'] = (
        200,
        json.dumps({
            'status': 'OK',
            'content': content
        })
    )
    setup_requests_call_mock(requestsGETMockObj, config)
