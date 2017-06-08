# -*- coding: utf-8 -*-
import wtforms

__all__ = ("EnumSelectField",)


def _simple_i18n(value):
    return str(value)


_unset_value = object()


class EnumSelectField(wtforms.SelectField):
    def __init__(self, enum_type, i18n=_simple_i18n, allow_none=False, *args, **kvargs):
        super(EnumSelectField, self).__init__(*args, **kvargs)
        self._enum_type = enum_type
        self.choices = []

        if allow_none:
            self.choices.append(allow_none if isinstance(allow_none, tuple) else (u"", u"(Please select)",))

        for element in self._enum_type.__elements__:
            self.choices.append((str(element.ordinal()), i18n(str(element)),))

    def as_constant(self):

        if not self.data or self.data == "None" or self.data is _unset_value:
            raise ValueError(
                u"invalid identifier for the registered type (data=%s, enum_type=%s)" % (self.data, self._enum_type))
        else:
            return self._enum_type.__elements__[int(self.data)]
