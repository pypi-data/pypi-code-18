from .session import Session
from .utils import list_wrapper


class ValueSerializer(object):
    def _check_needs_loading(self):
        """check if it needs to load the endpoint."""

    def serialize(self):
        """Custom serialize a value."""


def _apply_validate_func(validate_func, value):
    if validate_func:
        ret = validate_func(value)
        # a validate_func can raise specific ValidationError or can return falsy, to raise a generic ValidationError
        if not ret:
            raise ValidationError("Validation failed for value='%s'" % (value,))


def _single_attr_get(attr_name, default=None, custom_type=None):
    def _get(self):
        self._check_needs_loading()
        ret = self._content.get(attr_name, default)
        if ret is not None:
            if custom_type:
                cache_key = '%s%s' % (attr_name, custom_type.__name__)
                inst = self._cached_instances.get(cache_key)
                if inst is None:
                    inst = custom_type(content=ret, session=self.session)
                    self._cached_instances[cache_key] = inst
                ret = inst
            return ret
    return _get


def _single_attr_set(attr_name, attr_type, validate_func=None, transform_func=None):
    def _set(self, value):
        assert isinstance(value, attr_type) or value is None
        _apply_validate_func(validate_func, value)
        if transform_func:
            transform_func(self._content, attr_name, value)
        else:
            if isinstance(value, ValueSerializer):
                value = value.serialize()
            self._content[attr_name] = value
    return _set


def _attr_del(attr_name):
    def _del(self):
        del self._content[attr_name]
    return _del


def _multi_attr_get(attr_name, default=None, custom_type=None, readonly=False):
    def _get(self):
        self._check_needs_loading()
        ret = self._content.get(attr_name, default)
        if ret is not None:
            if custom_type:
                ret = list_wrapper(content=ret, custom_type=custom_type, readonly=readonly, session=self.session)
            return ret
    return _get


def _multi_attr_set(attr_name, list_elem_type, validate_func=None, transform_func=None):
    def _set(self, value):
        assert isinstance(value, list) or value is None
        assert all(isinstance(elem, list_elem_type) for elem in value)
        _apply_validate_func(validate_func, value)
        if transform_func:
            transform_func(self._content, attr_name, value)
        else:
            self._content[attr_name] = [v.serialize() if isinstance(v, ValueSerializer) else v for v in value]
    return _set


def make_single_elem_property(attr_name, elem_type, default=None, doc_string='', validate_func=None, transform_func=None, custom_type=None, readonly=False):
    return property(
        _single_attr_get(attr_name, default, custom_type=custom_type),
        None if readonly else _single_attr_set(attr_name, elem_type, validate_func=validate_func, transform_func=transform_func),
        None if readonly else _attr_del(attr_name),
        doc_string
    )


def make_multi_elem_property(attr_name, elem_type, doc_string='', validate_func=None, transform_func=None, custom_type=None, readonly=False):
    return property(
        _multi_attr_get(attr_name, default=[], custom_type=custom_type, readonly=readonly),
        None if readonly else _multi_attr_set(attr_name, elem_type, validate_func=validate_func, transform_func=transform_func),
        None if readonly else _attr_del(attr_name),
        doc_string
    )


def _single_ref_attr_get(attr_name, elem_ref_type):
    def _get(self):
        self._check_needs_loading()
        key = self._content.get(attr_name)
        if key:
            return self.session.get(elem_ref_type, key, lazy_load=True)
    return _get


def _single_ref_attr_set(attr_name, elem_ref_type, validate_func=None):
    def _set(self, value):
        if value is not None:
            assert isinstance(value, Session.enpoint_accepted_types(elem_ref_type))
            _apply_validate_func(validate_func, value)
            value = value.key
        self._content[attr_name] = value
    return _set


def make_single_elem_ref_property(attr_name, elem_ref_type, doc_string='', validate_func=None, readonly=False):
    return property(
        _single_ref_attr_get(attr_name, elem_ref_type),
        None if readonly else _single_ref_attr_set(attr_name, elem_ref_type, validate_func=validate_func),
        None if readonly else _attr_del(attr_name),
        doc_string
    )


def _multi_ref_attr_get(attr_name, elem_ref_type, readonly=False):
    def _get(self):
        self._check_needs_loading()
        keys = self._content.get(attr_name, [])
        return list_wrapper(keys, endpoint_type=elem_ref_type, readonly=readonly, session=self.session)
    return _get


def _multi_ref_attr_set(attr_name, elem_ref_type):
    def _set(self, value):
        if value is not None:
            assert isinstance(value, list)
            elem_ref_type_cls = Session.enpoint_accepted_types(elem_ref_type)
            assert all(isinstance(v, elem_ref_type_cls) for v in value)
            value = [v.key for v in value]
        self._content[attr_name] = value
    return _set


def make_multi_elem_ref_property(attr_name, elem_ref_type, doc_string='', readonly=False):
    return property(
        _multi_ref_attr_get(attr_name, elem_ref_type, readonly=readonly),
        None if readonly else _multi_ref_attr_set(attr_name, elem_ref_type),
        None if readonly else _attr_del(attr_name),
        doc_string
    )


def make_single_readonly_property(attr_name, default=None, doc_string=''):
    return property(_single_attr_get(attr_name, default=default), None, None, doc_string)


class ValidationError(Exception):
    """Raised when the validation of the instance fails before a save."""


class Endpoint(ValueSerializer):

    class VISIBILITY(object):
        PRIVATE = 'PRIVATE'
        EVERYONE = 'EVERYONE'
        GROUPS = 'GROUPS'

    def __init__(self, session, key=None, content=None, lazy_load=False):
        """
        Create an endpoint object.

        session - a Session instance
        key - the key (unique id) of the object. When creating a new object and before saving, this will be None
        content - when the content is provided, the instance is built from this content
        lazy_load - when True, the instance is only loaded from the server on the first property access
        """
        self.session = session
        if key is not None:
            try:
                key = int(key)
            except ValueError:
                pass
        self._key = key
        self._loaded = False
        self._cached_instances = {}
        if content is not None:
            self._content = content
        elif self.key and not lazy_load:
            self._load()
        else:
            self._content = {}
            if hasattr(self, 'DEFAULTS'):
                self._content.update(self.DEFAULTS)

    @classmethod
    def all(cls, session):
        ret = []
        content = session.make_request(cls.ENDPOINT)
        for endpoint_content in content:
            ret.append(cls(session, key=endpoint_content['id'], content=endpoint_content))
        return ret

    def _check_needs_loading(self):
        if self._key and not self._loaded:
            self._load()

    def serialize(self):
        return self.key

    def _load(self, reload=False):
        assert self._key, "Cannot load a resource without a key"
        load_all = getattr(self, 'LOAD_ALL', False)
        self._content = self.session.make_request(self.ENDPOINT, resource_id=self._key, load_all=load_all, reload=reload)
        self._loaded = True

    def reload(self):
        self._load(reload=True)

    def validate(self):
        """Validates the current instance before save.
        When it fails, validate raises a ValidationError exception."""

    def save(self):
        self.validate()
        method = 'PUT' if self._key else 'POST'
        ret = self.session.make_request(self.ENDPOINT, resource_id=self.key, method=method, payload=self._content)
        self._key = ret['id']
        self._content.update(ret)
        self._loaded = True

    def delete(self):
        self.session.make_request(self.ENDPOINT, resource_id=self._key, method='DELETE')
        self._key = None

    def is_new(self):
        return not self._key

    def get_content(self):
        # get the raw content for this endpoint - avoid using directly
        return self._content

    @property
    def key(self):
        return self._key

    @property
    def visibility(self):
        self._check_needs_loading()
        if self._content.get('is_private', False):
            return self.VISIBILITY.PRIVATE
        if self._content.get('gid', 0):
            return self.VISIBILITY.GROUPS
        return self.VISIBILITY.EVERYONE

    private_to = make_single_elem_ref_property('puser', 'User', 'The user this item is private to (if any).')

    def get_groups(self):
        self._check_needs_loading()
        groups = []
        gid = self._content.get('gid', 0)
        if gid:
            from .user import Group  # avoid cyclical import
            groups = []
            for group in Group.all(self.session):
                if group.gid & gid:
                    groups.append(group)
        return tuple(groups)

    def set_groups(self, groups):
        assert isinstance(groups, (list, tuple))
        self._content['gid'] = sum([group.gid for group in groups])

    @property
    def added_on(self):
        self._check_needs_loading()
        return self._content.get('ao')

    @property
    def last_modified(self):
        self._check_needs_loading()
        return self._content.get('lm')

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s' % (self._content,)
