import xmltodict

from roundhouse import Serializer


class XMLSerializer(Serializer):

    format = 'xml'
    extensions = ['.xml']

    def serialize(self, data, stream):
        serialized = xmltodict.unparse(data, pretty=self.pretty)

        stream.write(serialized.encode())

        return stream

    def deserialize(self, stream):
        # Expects bytes internally, but accepts full string
        return xmltodict.parse(stream)
