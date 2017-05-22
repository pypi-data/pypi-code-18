# -*- coding: utf-8 -*-

import json
import sys

from google.protobuf.descriptor_pb2 import DescriptorProto, EnumDescriptorProto

from grpc_pytools.generator import Generator


class DigestGenerator(Generator):

    def _make_data(self, response, proto_file):
        return {'haha': 'hehe'}

    def _add_data(self, response, proto_file):
        data = self._make_data()
        f = response.file.add()
        f.name = proto_file.name + '.json'
        f.content = json.dumps(data, indent=2)


def main():
    DigestGenerator(sys.stdin, sys.stdout).generate()


if __name__ == '__main__':
    main()
