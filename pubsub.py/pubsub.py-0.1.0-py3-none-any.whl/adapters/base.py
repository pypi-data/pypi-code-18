import re
import jsonschema


class BaseAdapter(object):
    """
    PubSub adapter base class
    """

    def __init__(self):
        pass

    def validate_message(self, message):
        if not message.get('schema', None):
            raise ValueError('Message must contain a schema!')
        schema_uri = message['schema']
        matches = re.findall(r'(.+)://(.+/)?events/(.+)/(.+)/(.+)\.json', schema_uri)[0]
        if matches:
            schema = jsonschema.RefResolver('', '').resolve_remote(schema_uri)
            jsonschema.validate(message, schema)
        else:
            raise ValueError('Incorrect schema uri')

    def publish(self, channel, message, **kwargs):
        raise NotImplementedError('Not implemented')

    def subscribe(self, channel, handler=lambda x: x, **kwargs):
        raise NotImplementedError('Not implemented')


class IdentifierRequiredException(Exception):
    pass
