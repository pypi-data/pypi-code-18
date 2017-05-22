# -*- coding: utf-8 -*-

import json
import os
import sys

from .generator import Generator


class DigestGenerator(Generator):

    def _make_data(self, proto_file):
        # Toplevel info
        data = dict(
            name=proto_file.name,
            syntax=proto_file.syntax,
            package=proto_file.package,
        )

        # Enum info
        enums = []
        for enum in proto_file.enum_type:
            # print(dir(enum))
            break
        data['enums'] = enums

        # Message info
        messages = []
        for message in proto_file.message_type:
            # print(dir(message.field[0]))
            # break
            messages.append(dict(
                name=message.name,
                fields=[
                    dict(
                        type=self._types_map[field.type].name,
                        type_name=field.type_name,
                        name=field.name,
                        label=self._labels_map[field.label].name,
                        number=field.number
                    )
                    for field in message.field
                ]
            ))
        data['messages'] = messages

        # Service info
        services = []
        for service in proto_file.service:
            services.append(dict(
                name=service.name,
                methods=[
                    dict(
                        name=method.name,
                        input_type=method.input_type,
                        output_type=method.output_type
                    )
                    for method in service.method
                ]
            ))
        data['services'] = services

        return data

    def _make_file(self, proto_file):
        data = self._make_data(proto_file)
        name = (
            os.path.splitext(os.path.basename(proto_file.name))[0]
            + '_digest.json'
        )
        content = json.dumps(data, indent=2)
        return name, content


def main():
    DigestGenerator(sys.stdin, sys.stdout).generate()


if __name__ == '__main__':
    main()
