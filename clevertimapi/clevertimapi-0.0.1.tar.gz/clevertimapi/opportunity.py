from .compat import string_types
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property, make_single_elem_ref_property
from .session import Session
from .customfield import OpportunitiesCustomFieldValueCollection


class Opportunity(Endpoint):

    ENDPOINT = '/opportunity'

    DEFAULTS = {
        'cf': {}
    }

    name = make_single_elem_property('name', string_types, '', 'Opportunity headline text')
    description = make_single_elem_property('description', string_types, '', 'Some text about this opportunity')
    lead_user = make_single_elem_ref_property('leadUser', 'User', 'The user this opportunity is assigned to')
    who = make_single_elem_ref_property('cust', 'ContactOrCompany', 'The contact or company this task is for')

    currency = make_single_elem_property('currency', string_types, '', 'The currency code (e.g. USD, EUR, GBP)')
    value = make_single_elem_property('value', string_types, '', 'The value of this deal')
    status = make_single_elem_property('status', string_types, '', 'The pipeline state of this opportunity')

    tags = make_multi_elem_property('tags', string_types, 'List of tags this opportunity was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this oppotunity')
    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this opportunity')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this opportunity')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this opportunity')

    custom_field_values = make_single_elem_property('cf', OpportunitiesCustomFieldValueCollection, {}, 'Opportunity\'s list of custom field values', custom_type=OpportunitiesCustomFieldValueCollection)

    created_by = make_single_elem_ref_property('userId', 'User', 'The user who created this opportunity', readonly=True)


Session.register_endpoint(Opportunity)
