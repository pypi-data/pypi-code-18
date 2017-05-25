from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property, make_single_elem_ref_property
from .customfield import CasesCustomFieldValueCollection


class Case(Endpoint):

    ENDPOINT = '/case'

    DEFAULTS = {
        'cf': {}
    }

    name = make_single_elem_property('name', string_types, '', 'Case headline description')
    description = make_single_elem_property('description', string_types, '', 'Some text about this case')
    lead_user = make_single_elem_ref_property('leadUser', 'User', 'The user this case is assigned to')
    who = make_single_elem_ref_property('cust', 'ContactOrCompany', 'The contact or company this task is for')

    tags = make_multi_elem_property('tags', string_types, 'List of tags this case was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this case')
    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this case')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this case')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this case')

    custom_field_values = make_single_elem_property('cf', CasesCustomFieldValueCollection, {}, 'Case\'s list of custom field values', custom_type=CasesCustomFieldValueCollection)


Session.register_endpoint(Case)
