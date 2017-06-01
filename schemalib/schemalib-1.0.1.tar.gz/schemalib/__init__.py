import jsonschema
import json
import pkgutil
import errno
from os import path


PKG_PREFIX = 'package://'
SCHEMA_SUFFIX = '.json'


class SchemaArgumentError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


class Schema(object):
    def __init__(self, name, schema):
        """Initialize schema object

        :param name: name of the schema file
        :type name: str
        :param schema: schema contents
        :type schema: str
        """

        self.name = name
        self.schema = schema

    def check(self, data):
        """Check the validity of data against this schema

        :param data: Input object to check
        :raises: jsonschema.ValidationError
        """

        jsonschema.validate(data, self.schema)


class SchemaLibrary(dict):
    def __init__(self, *base_paths):
        """Initialize schema library object

        :param base_paths: paths where to look when looking for a schema
        :type base_paths: str
        """

        self._base_paths = list(base_paths)
        super().__init__()

    def load_schema(self, name):
        """Load schema specified by name, searching `base_paths` sequentially

        :param name: schema name
        :type name: str
        :return: schema contents as string
        :rtype: str
        :raises: schemalib.SchemaNotFoundError when the schema couldn't be found
        """

        for p in self._base_paths:
            if p.startswith(PKG_PREFIX):
                stripped, data = p[len(PKG_PREFIX):], None
                try:
                    data = pkgutil.get_data(stripped, name + SCHEMA_SUFFIX)
                except IOError as err:
                    if err.errno == errno.ENOENT:
                        continue
                if data:
                    return data
            else:
                lookup = path.join(p, name) + SCHEMA_SUFFIX
                if path.exists(lookup):
                    with open(lookup, 'r') as f:
                        return f.read()

        raise SchemaNotFoundError(name)

    def __getitem__(self, item):
        """Caching wrapper around __getitem__ that lazily loads schemas from disk

        :param item: Schema name to look up
        :type item: str
        :return: Schema object
        :rtype: schemalib.Schema
        """

        if item not in self:
            schema = Schema(item, json.loads(self.load_schema(item)))
            self[item] = schema
        return super(SchemaLibrary, self).__getitem__(item)

    def check(self, *args, **kwargs):
        """ Function decorator that allows for return value and keyword parameter schema validation """

        schema = args[0] if len(args) > 0 else None
        schemas = dict(kwargs)

        def wrapped(f):
            def inner(*iargs, **ikwargs):
                for k, v in schemas.items():
                    if k not in ikwargs:
                        raise SchemaArgumentError('Argument does not exist: {}'.format(k))
                    self[v].check(ikwargs[k])
                v = f(*iargs, **ikwargs)
                if schema:
                    self[schema].check(v)
                return v
            return inner
        return wrapped
