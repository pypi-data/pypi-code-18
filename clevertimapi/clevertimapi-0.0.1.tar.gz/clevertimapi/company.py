from .compat import string_types
from .contact import PhoneNumber, SocialMediaId, Contact
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property
from .session import Session, SessionError
from .customfield import CompaniesCustomFieldValueCollection


class Company(Endpoint):

    ENDPOINT = '/company'

    DEFAULTS = {
        'is_company': True,
        'cf': {}
    }

    name = make_single_elem_property('cn', string_types, '', 'Company\'s name')

    address = make_single_elem_property('address', string_types, '', 'Company\'s address')
    city = make_single_elem_property('city', string_types, '', 'Company\'s city')
    postcode = make_single_elem_property('postcode', string_types, '', 'Company\'s postcode')
    region = make_single_elem_property('region', string_types, '', 'Company\'s region/district/state code')
    country = make_single_elem_property('country', string_types, '', 'Company\'s country code')

    description = make_single_elem_property('description', string_types, '', 'Some text about this company')

    emails = make_multi_elem_property('email', string_types, 'Company\'s list of email addresses')
    websites = make_multi_elem_property('website', string_types, 'Company\'s list of web sites')
    phone_numbers = make_multi_elem_property('phones', PhoneNumber, 'Company\'s list of phone numbers', custom_type=PhoneNumber)
    social_media_ids = make_multi_elem_property('smids', SocialMediaId, 'Company\'s list of social media ids', custom_type=SocialMediaId)

    tags = make_multi_elem_property('tags', string_types, 'List of tags this company was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this company')
    opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this company')
    cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this company')

    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this company')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this contact')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this contact')

    custom_field_values = make_single_elem_property('cf', CompaniesCustomFieldValueCollection, {}, 'Company\'s list of custom field values', custom_type=CompaniesCustomFieldValueCollection)

    @property
    def last_contacted(self):
        self._check_needs_loading()
        return self._content.get('lc')

    @property
    def company_logo(self):
        """The url to the company logo (an image)."""
        self._check_needs_loading()
        cphoto = self._content.get('cphoto')
        if cphoto:
            url = self.session.url
            if url.endswith('/api'):
                url = url[:-4]
            return url + '/getcphoto/%s/%s' % (self.key, cphoto)


def create_contact_or_company(session, key, lazy_load=False):
    assert isinstance(session, Session)
    try:
        return Contact(session, key=key)
    except SessionError:
        pass
    return Company(session, key=key)


Session.register_endpoint(Company)
Session.register_endpoint_factory('ContactOrCompany', create_contact_or_company, accepted_types=(Contact, Company))
