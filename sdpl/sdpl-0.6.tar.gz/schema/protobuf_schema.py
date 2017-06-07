__author__ = 'Bohdan Mushkevych'

from google.protobuf import message, descriptor

from schema import sdpl_schema

# `google.protobuf.descriptor.FieldDescriptor`
DESCRIPTOR_TYPES = {
    1: 'TYPE_DOUBLE',
    2: 'TYPE_FLOAT',
    3: 'TYPE_INT64',
    4: 'TYPE_UINT64',
    5: 'TYPE_INT32',
    6: 'TYPE_FIXED64',
    7: 'TYPE_FIXED32',
    8: 'TYPE_BOOL',
    9: 'TYPE_STRING',
    10: 'TYPE_GROUP',
    11: 'TYPE_MESSAGE',
    12: 'TYPE_BYTES',
    13: 'TYPE_UINT32',
    14: 'TYPE_ENUM',
    15: 'TYPE_SFIXED32',
    16: 'TYPE_SFIXED64',
    17: 'TYPE_SINT32',
    18: 'TYPE_SINT64'
}

# `google.protobuf.descriptor.FieldDescriptor`
PROTOBUF_MAPPING = {
    'TYPE_INT32': sdpl_schema.FieldType.INTEGER,
    'TYPE_UINT32': sdpl_schema.FieldType.INTEGER,
    'TYPE_FIXED32': sdpl_schema.FieldType.INTEGER,
    'TYPE_INT64': sdpl_schema.FieldType.LONG,
    'TYPE_UINT64': sdpl_schema.FieldType.LONG,
    'TYPE_FIXED64': sdpl_schema.FieldType.LONG,
    'TYPE_ENUM': sdpl_schema.FieldType.CHARARRAY,
    'TYPE_LONG': sdpl_schema.FieldType.LONG,
    'TYPE_FLOAT': sdpl_schema.FieldType.FLOAT,
    'TYPE_DOUBLE': sdpl_schema.FieldType.FLOAT,
    'TYPE_STRING': sdpl_schema.FieldType.CHARARRAY,
    'TYPE_NULL': sdpl_schema.FieldType.BYTEARRAY,
    'TYPE_BYTES': sdpl_schema.FieldType.BYTEARRAY,
    'TYPE_BOOL': sdpl_schema.FieldType.BOOLEAN,
    'Timestamp': sdpl_schema.FieldType.DATETIME,
}


class ProtobufSchema(object):
    def __init__(self, proto_schema: message.Message) -> None:
        self.proto_schema = proto_schema

    def _parse_descriptor(self, schema_element: descriptor.FieldDescriptor):
        field_name = schema_element.name
        proto_type_str = DESCRIPTOR_TYPES[schema_element.type]
        sdpl_field_type = PROTOBUF_MAPPING[proto_type_str]
        default_value = None if not schema_element.has_default_value else schema_element.default_value
        is_nullable = False
        return sdpl_schema.Field(field_name, sdpl_field_type, default=default_value, is_nullable=is_nullable)

    def _parse_message(self, msg: message.Message):
        s = sdpl_schema.Schema()
        for element in msg.DESCRIPTOR.fields:
            if element.type == element.TYPE_MESSAGE:
                s.fields.append(self._parse_message(element))
            else:
                s.fields.append(self._parse_descriptor(element))
        return s

    def to_sdpl_schema(self):
        return self._parse_message(self.proto_schema)
