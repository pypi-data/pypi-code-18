from .compat import string_types
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property, ValueSerializer, ValidationError
from .session import Session
from .customfield import ContactsCustomFieldValueCollection


class PhoneNumber(ValueSerializer):

    class PHONE_TYPES(object):
        WORK = 'Work'
        HOME = 'Home'
        MOBILE = 'Mobile'
        FAX = 'Fax'
        PAGER = 'Pager'

        ALL_VALID_VALUES = frozenset((WORK, HOME, MOBILE, FAX, PAGER))

        @classmethod
        def is_valid_phone_type(cls, value):
            if value not in cls.ALL_VALID_VALUES:
                raise ValidationError("Invalid phone type '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_VALUES)))
            return True

    def __init__(self, content=None, phone_number=None, phone_type=None, session=None):
        self._content = {}
        if content:
            phone_number = content.get('no')
            phone_type = content.get('type')
        if phone_type is not None:
            self.phone_type = phone_type
        if phone_number is not None:
            self.phone_number = phone_number

    phone_number = make_single_elem_property('no', string_types, '', 'Phone number')
    phone_type = make_single_elem_property('type', string_types, '', 'Phone type: Work, Home, Mobile, Fax or Pager', validate_func=PHONE_TYPES.is_valid_phone_type)

    def serialize(self):
        no = self._content.get('no')
        if not no or not isinstance(no, string_types):
            raise ValidationError("Invalid phone number.")
        phone_type = self._content.get('type')
        self.PHONE_TYPES.is_valid_phone_type(phone_type)
        return self._content

    def __eq__(self, other):
        return self.phone_number == other.phone_number and self.phone_type == other.phone_type

    def __ne__(self, other):
        return not self.__eq__(other)


class SocialMediaId(ValueSerializer):

    class SOCIAL_MEDIA_VENUES(object):
        BITBUCKET = 'BitBucket'
        FACEBOOK = 'Facebook'
        GITHUB = 'Github'
        GOOGLEPLUS = 'Google+'
        INSTAGRAM = 'Instagram'
        KIK = 'Kik'
        LINKEDIN = 'LinkedIn'
        MSN = 'MSN'
        PINTEREST = 'Pinterest'
        REDDIT = 'Reddit'
        SKYPE = 'Skype'
        SNAPCHAT = 'Snapchat'
        TELEGRAM = 'Telegram'
        TWITTER = 'Twitter'
        WHATSAPP = 'Whatsapp'
        YOUTUBE = 'YouTube'

        ALL_VALID_VALUES = frozenset((
            BITBUCKET,
            FACEBOOK,
            GITHUB,
            GOOGLEPLUS,
            INSTAGRAM,
            KIK,
            LINKEDIN,
            MSN,
            PINTEREST,
            REDDIT,
            SKYPE,
            SNAPCHAT,
            TELEGRAM,
            TWITTER,
            WHATSAPP,
            YOUTUBE,
        ))

        @classmethod
        def is_valid_social_media_type(cls, value):
            if value not in cls.ALL_VALID_VALUES:
                raise ValidationError("Invalid phone type '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_VALUES)))
            return True

    def __init__(self, content=None, social_media_id=None, social_media_type=None, session=None):
        self._content = {}
        if content:
            social_media_id = content.get('smid')
            social_media_type = content.get('type')
        if social_media_type is not None:
            self.social_media_type = social_media_type
        if social_media_id is not None:
            self.social_media_id = social_media_id

    social_media_id = make_single_elem_property('smid', string_types, '', 'Social media id')
    social_media_type = make_single_elem_property('type', string_types, '', 'Social media venue', validate_func=SOCIAL_MEDIA_VENUES.is_valid_social_media_type)

    def serialize(self):
        social_media_id = self._content.get('smid')
        if not social_media_id or not isinstance(social_media_id, string_types):
            raise ValidationError("Invalid social media type.")
        social_media_type = self._content.get('type')
        self.SOCIAL_MEDIA_VENUES.is_valid_social_media_type(social_media_type)
        return self._content

    def __eq__(self, other):
        return self.social_media_id == other.social_media_id and self.social_media_type == other.social_media_type

    def __ne__(self, other):
        return not self.__eq__(other)


class Contact(Endpoint):

    ENDPOINT = '/contact'

    DEFAULTS = {
        'is_company': False,
        'cf': {}
    }

    first_name = make_single_elem_property('fn', string_types, '', 'Contact\'s first name')
    last_name = make_single_elem_property('ln', string_types, '', 'Contact\'s last name')
    title = make_single_elem_property('title', string_types, '', 'Contact\'s title')

    company = make_single_elem_ref_property('companyId', 'Company', 'Contact\'s company')

    address = make_single_elem_property('address', string_types, '', 'Contact\'s address')
    city = make_single_elem_property('city', string_types, '', 'Contact\'s city')
    postcode = make_single_elem_property('postcode', string_types, '', 'Contact\'s postcode')
    region = make_single_elem_property('region', string_types, '', 'Contact\'s region/district/state code')
    country = make_single_elem_property('country', string_types, '', 'Contact\'s country code')

    description = make_single_elem_property('description', string_types, '', 'Some text about this contact')

    emails = make_multi_elem_property('email', string_types, 'Contact\'s list of email addresses')
    websites = make_multi_elem_property('website', string_types, 'Contact\'s list of web sites')
    phone_numbers = make_multi_elem_property('phones', PhoneNumber, 'Contact\'s list of phone numbers', custom_type=PhoneNumber)
    social_media_ids = make_multi_elem_property('smids', SocialMediaId, 'Contact\'s list of social media ids', custom_type=SocialMediaId)

    tags = make_multi_elem_property('tags', string_types, 'List of tags this contact was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this contact')
    opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this contact')
    cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this contact')

    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this contact')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this contact')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this contact')

    custom_field_values = make_single_elem_property('cf', ContactsCustomFieldValueCollection, {}, 'Contact\'s list of custom field values', custom_type=ContactsCustomFieldValueCollection)

    @property
    def last_contacted(self):
        self._check_needs_loading()
        return self._content.get('lc')

    @property
    def contact_photo(self):
        """The url to the contact photo (an image)."""
        self._check_needs_loading()
        cphoto = self._content.get('cphoto')
        if cphoto:
            url = self.session.url
            if url.endswith('/api'):
                url = url[:-4]
            return url + '/getcphoto/%s/%s' % (self.key, cphoto)


Session.register_endpoint(Contact)
