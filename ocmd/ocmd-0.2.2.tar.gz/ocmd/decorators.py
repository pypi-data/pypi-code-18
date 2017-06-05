import logging
from functools import update_wrapper

import click
from .connection import Connection
from .param import OssDestType


def get_connection(f):
    @click.argument("dest", type=OssDestType(), required=True)
    @click.option("--access_key", envvar="OSS_ACCESS_KEY")
    @click.option("--secret_key", envvar="OSS_SECRET_KEY")
    @click.option("--endpoint", envvar="OSS_ENDPOINT")
    @click.option("-v", "--verbose", envvar="OSS_VERBOSE", is_flag=True)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        dest = kwargs["dest"]
        access_key = kwargs.pop("access_key", None)
        secret_key = kwargs.pop("secret_key", None)
        endpoint = kwargs.pop("endpoint", None)
        conn = Connection(
            access_key, secret_key,
            dest.bucket, endpoint=endpoint
        )
        if kwargs.pop("verbose"):
            fmt = logging.Formatter(u"[{0}] %(message)s".format(dest.bucket))
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(fmt)

            logger = logging.getLogger("ocmd")
            logger.setLevel(logging.INFO)
            logger.addHandler(ch)

        return ctx.invoke(f, conn, *args, **kwargs)
    return update_wrapper(wrapper, f)
