from .compat import string_types
from .session import Session


class custom_type_adapter(object):
    def __init__(self, custom_type_instance):
        from .endpoint import ValueSerializer  # to prevent a circular import
        assert isinstance(custom_type_instance, ValueSerializer), "Unsupported value:'%s'" % (custom_type_instance,)
        self.custom_type_instance = custom_type_instance

    def get_instance(self):
        return self.custom_type_instance

    def to_value(self):
        return self.custom_type_instance.serialize()

    def __eq__(self, other):
        if isinstance(other, custom_type_adapter):
            return self.custom_type_instance == other.custom_type_instance
        return self.custom_type_instance == other

    def __ne__(self, other):
        return not self.__eq__(other)


class list_wrapper(object):
    def __init__(self, content, endpoint_type=None, custom_type=None, readonly=False, session=None):
        from .endpoint import Endpoint, ValueSerializer  # to prevent a circular import
        assert isinstance(content, list)
        assert not all([endpoint_type, custom_type])
        self._content = content
        self._endpoint_type = endpoint_type
        self._custom_type = custom_type
        self.allowed_types = tuple(filter(None, [endpoint_type, custom_type]))
        self._session = session
        if self._endpoint_type:
            assert isinstance(session, Session)
            assert isinstance(self._endpoint_type, string_types) or issubclass(self._endpoint_type, Endpoint), "Unsupported endpoint type: '%s'" % (self._endpoint_type,)
            self._typed_content = [
                custom_type_adapter(session.get(self._endpoint_type, key, lazy_load=True)) for key in self._content
            ]
        elif self._custom_type:
            assert isinstance(session, Session)
            assert issubclass(self._custom_type, ValueSerializer), "Unsupported custom type: '%s'" % (self._custom_type,)
            self._typed_content = [
                custom_type_adapter(custom_type(content=ct, session=session)) for ct in self._content
            ]
        else:
            self._typed_content = None
        self._readonly = readonly

    def append(self, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content is not None:
            assert isinstance(item, self.allowed_types)
            instance_wrapper = custom_type_adapter(item)
            self._typed_content.append(instance_wrapper)
            self._content.append(instance_wrapper.to_value())
        else:
            self._content.append(item)

    def extend(self, iterable):
        assert not self._readonly, "Cannot modify a readonly property"
        for item in iterable:
            self.append(item)

    def insert(self, idx, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content is not None:
            assert isinstance(item, self.allowed_types)
            instance_wrapper = custom_type_adapter(item)
            self._typed_content.insert(idx, instance_wrapper)
            self._content.insert(idx, instance_wrapper.to_value())
        else:
            self._content.insert(idx, item)

    def remove(self, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content is not None:
            assert isinstance(item, self.allowed_types)
            instance_wrapper = custom_type_adapter(item)
            self._typed_content.remove(instance_wrapper)
            self._content.remove(instance_wrapper.to_value())
        else:
            self._content.remove(item)

    def pop(self, idx=-1):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content is not None:
            self._content.pop(idx)
            instance_wrapper = self._typed_content.pop(idx)
            return instance_wrapper.get_instance()
        else:
            return self._content.pop(idx)

    def clear(self):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content is not None:
            del self._typed_content[:]
        del self._content[:]

    def __getitem__(self, idx):
        if self._typed_content is not None:
            instance_wrapper = self._typed_content[idx]
            return instance_wrapper.get_instance()
        else:
            return self._content[idx]

    def __setitem__(self, idx, value):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content:
            assert isinstance(value, self.allowed_types)
            instance_wrapper = custom_type_adapter(value)
            self._typed_content[idx] = instance_wrapper
            self._content[idx] = instance_wrapper.to_value()
        else:
            self._content[idx] = value

    def __delitem__(self, idx):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._typed_content:
            del self._typed_content[idx]
        del self._content[idx]

    def __len__(self):
        if self._typed_content is not None:
            assert len(self._typed_content) == len(self._content)
            return len(self._typed_content)
        else:
            return len(self._content)

    def __iter__(self):
        if self._typed_content is not None:
            for item in self._typed_content:
                yield item.get_instance()
        else:
            for item in self._content:
                yield item

    def __eq__(self, other):
        if self._typed_content is not None:
            return self._typed_content == other
        return self._content == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iadd__(self, iterable):
        self.extend(iterable)
        return self
