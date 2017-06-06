from base.fields import (
    BaseField,
    STRING,
)

AVAILABLE_KEY_FIELDS = (
    'HashKeyField', 'RangeKeyField', )
AVAILABLE_FIELDS = (
    'StringField', )


class HashKeyField(BaseField):
    KEY_TYPE = 'HASH'

    def __init__(self, type):
        self.ATTRIBUTE_TYPE = type


class RangeKeyField(BaseField):
    KEY_TYPE = 'RANGE'

    def __init__(self, type):
        self.ATTRIBUTE_TYPE = type


class StringField(BaseField):
    ATTRIBUTE_TYPE = STRING
