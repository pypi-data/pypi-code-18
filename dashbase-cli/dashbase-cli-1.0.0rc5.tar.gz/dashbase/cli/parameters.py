import re

import click

from dashbase.cli.constants import DEFAULT_MIRROR
from dashbase.services import VersionService


class NameParamType(click.ParamType):
    name = 'name'

    def convert(self, value, param, ctx):
        if not re.match("^[A-Za-z0-9_-]*$", value):
            self.fail(
                """{}\nLimited to the set of alphanumeric characters [a-zA-Z0-9], and punctuation characters [._-]""".format(
                    value), param, ctx)
        if not 3 < len(value) < 30:
            self.fail("""{}\nName length should be 3 - 30 characters""".format(
                value), param, ctx)
        return value


class EnvParamType(click.ParamType):
    name = 'string {key=value}'

    def convert(self, value, param, ctx):
        try:
            key, value = value.split("=")
            return key, value
        except ValueError:
            self.fail("""{}\nIncorrect format! e.g ADMINPORT=12345""".format(
                value), param, ctx)


class MirrorParamType(click.ParamType):
    name = 'mirror_url'

    def convert(self, value, param, ctx):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not regex.match(value):
            self.fail("Please input a valid url.")

        return value


class VersionParamType(click.ParamType):
    name = 'version'

    def convert(self, value, param, ctx):
        available_versions = VersionService.get_available_versions(DEFAULT_MIRROR)
        if value not in available_versions:
            click.secho('Available versions are:', fg='yellow')
            for version in available_versions:
                click.secho(version, fg='yellow')
            click.echo()
            self.fail("Please input a valid version.")

        return value


NAME = NameParamType()
ENV = EnvParamType()
MIRROR = MirrorParamType()
VERSION = VersionParamType()
