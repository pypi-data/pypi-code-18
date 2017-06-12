from __future__ import absolute_import

from collections import OrderedDict

import yaml
from roundhouse import Serializer

yaml.add_representer(OrderedDict, lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items()))
yaml.SafeLoader.add_constructor("tag:yaml.org,2002:python/unicode", lambda self, data: data.value)


class YAMLSerializer(Serializer):
    """Handles serialization of YAML data"""

    format = 'yaml'
    extensions = ['.yml', '.yaml']

    def serialize(self, data, stream):
        stream.write(yaml.dump(data, default_flow_style=not self.pretty).encode())

        return stream

    def deserialize(self, stream):
        return yaml.safe_load(stream)
