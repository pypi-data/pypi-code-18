import json

from django.contrib.postgres.forms.jsonb import InvalidJSONInput, JSONField
from django.forms import ValidationError


class JSONPrettyField(JSONField):
    def __init__(self, *args, **kwargs):
        self.__indent = kwargs.pop('indent', 2)
        self.__dict_only = kwargs.pop('dict_only', False)
        self.__list_only = kwargs.pop('list_only', False)
        if self.__dict_only and self.__list_only:
            raise ValueError('Only one of dict_only or list_only can be True')
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value, indent=self.__indent, sort_keys=True, ensure_ascii=False)

    def validate(self, value):
        if self.__dict_only and not isinstance(value, dict):
            raise ValidationError('{} is not of type dict'.format(value))
        if self.__list_only and not isinstance(value, list):
            raise ValidationError('{} is not of type list'.format(value))
        return value
