from collections import namedtuple

import click

Dest = namedtuple("OssDest", ["bucket", "dest"])


class OssDestType(click.ParamType):
    name = "oss-dest"

    def convert(self, value, param, ctx):
        try:
            bucket, dest = value.split(":", 1)
            dest = dest.lstrip("/")
            return Dest(bucket, dest)
        except ValueError:
            self.fail("{0} is not a valid oss dest".format(value), param, ctx)
