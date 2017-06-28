from marshmallow import Schema, fields, validate


class MetadataSchema(Schema):
    name = fields.String(required=True)
    username = fields.String()
    labels = fields.List(fields.String())

class GenericSchema(Schema):
    VERSIONS = ['v1']
    KINDS = ['User', 'Cluster', 'Structure', 'Calculation']

    version = fields.String(required=True, validate=validate.OneOf(VERSIONS))
    kind = fields.String(required=True, validate=validate.OneOf(KINDS))
    metadata = fields.Nested(MetadataSchema)
