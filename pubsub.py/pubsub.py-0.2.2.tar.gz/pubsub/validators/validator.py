import re
import jsonschema
from jsonschema import ValidationError


class SchemaValidator():
    """
    Validates pubsub messages against specified schema
    """

    def validate_message(self, message):
        try:
            message['schema']
        except KeyError:
            raise KeyError('Message must contain a schema!')
        except TypeError:
            raise TypeError('Message must be json')
        schema_uri = message.get('schema', '')
        matches = re.findall(r'(.+)://(.+/)?events/(.+)/(.+)/(.+)\.json', schema_uri)
        if len(matches) >= 1:
            schema = jsonschema.RefResolver('', '').resolve_remote(schema_uri)
            jsonschema.validate(message, schema)
        else:
            raise ValidationError('Incorrect schema uri')
