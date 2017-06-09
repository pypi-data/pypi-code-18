import json
from coreapi.codecs.base import BaseCodec
from coreapi.compat import COMPACT_SEPARATORS, VERBOSE_SEPARATORS
from coreapi.compat import force_bytes
from coreapi.document import Document
from coreapi.exceptions import ParseError
from .encode import generate_spore_object
from .decode import parse_spore_description


class SporeDescriptionCodec(BaseCodec):

    media_type = 'application/sporeapi+json'
    format = 'spore'

    def decode(self, bytestring, **options):
        try:
            spore_desc = json.loads(bytestring.decode('utf-8'))
        except ValueError as exc:
            raise ParseError('Malformed JSON. %s' % exc)

        base_url = options.get('base_url', '')
        coreapi_doc = parse_spore_description(spore_desc, base_url)
        if not isinstance(coreapi_doc, Document):
            raise ParseError('Top level node must be a document.')

        return coreapi_doc

    def encode(self, document, **options):
        if not isinstance(document, Document):
            raise TypeError('Expected a `coreapi.Document` instance')

        indent = options.get('indent', None)

        kwargs = {
            'ensure_ascii': False, 'indent': indent,
            'separators': indent and VERBOSE_SEPARATORS or COMPACT_SEPARATORS
        }

        global_formats = options.get('formats', [])
        spore_settings = options.get('settings', [])

        data = generate_spore_object(document, global_formats, spore_settings)
        return force_bytes(json.dumps(data, **kwargs))


