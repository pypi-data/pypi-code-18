__author__ = 'Bohdan Mushkevych'

import avro.schema

from schema import sdpl_schema

# `https://avro.apache.org/docs/1.8.1/spec.html#schema_primitive`
AVRO_MAPPING = {
    'int': sdpl_schema.FieldType.INTEGER,
    'long': sdpl_schema.FieldType.LONG,
    'float': sdpl_schema.FieldType.FLOAT,
    'double': sdpl_schema.FieldType.FLOAT,
    'string': sdpl_schema.FieldType.CHARARRAY,
    'null': sdpl_schema.FieldType.BYTEARRAY,
    'bytes': sdpl_schema.FieldType.BYTEARRAY,
    'boolean': sdpl_schema.FieldType.BOOLEAN,
    'UNDEFINED': sdpl_schema.FieldType.DATETIME,
}


class AvroSchema(object):
    def __init__(self, avro_schema: avro.schema.Schema) -> None:
        self.avro_schema = avro_schema

    def to_sdpl_schema(self):
        def _to_sdpl_field(avro_field):
            if isinstance(avro_field.type, avro.schema.PrimitiveSchema):
                # "type": "string"
                avro_field_type = avro_field.type.type
                is_nullable = False
            elif isinstance(avro_field.type, avro.schema.UnionSchema):
                # "type": ["string", "null"]
                types = set(t.type for t in avro_field.type.schemas)
                if len(types) > 2 or 'null' not in types:
                    raise ValueError('SDPL does not supports AVRO field {0} with types {1}'.
                                     format(avro_field.name, avro_field.type))

                types.remove('null')
                avro_field_type = types.pop()
                is_nullable = True
            else:
                raise ValueError(
                    'SDPL does not supports AVRO field {0} with types {1}'.format(avro_field.name, avro_field.type)
                )

            sdpl_field_type = AVRO_MAPPING[avro_field_type]
            default_value = None if not avro_field.has_default else avro_field.default
            return sdpl_schema.Field(avro_field.name, sdpl_field_type, default=default_value, is_nullable=is_nullable)

        s = sdpl_schema.Schema()
        for f in self.avro_schema.fields:
            assert isinstance(f, avro.schema.Field)
            s.fields.append(_to_sdpl_field(f))
        return s
