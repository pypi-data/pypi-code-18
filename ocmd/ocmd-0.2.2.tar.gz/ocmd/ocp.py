import logging
import os

import click
from .decorators import get_connection


logger = logging.getLogger(__name__)


@click.command()
@click.argument("src", nargs=-1, type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True)
@get_connection
def ocp(conn, dest, src, recursive):
    files = []
    errors = []
    for fp in src:
        if os.path.isdir(fp):
            if recursive:
                files.extend(
                    os.path.join(root, filename)
                    for root, dirnames, filenames in os.walk(fp)
                    for filename in filenames
                )
            else:
                errors.append(fp)
        else:
            files.append(fp)
    if errors:
        logger.error(u"{0} are folders".format(", ".join(errors)))
        raise ValueError(errors)
    for fp in files:
        with open(fp, "rb") as f:
            if fp.startswith(dest.dest):
                remote_name = fp
            else:
                remote_name = os.path.join(dest.dest, fp.lstrip("/"))
            remote_name = os.path.normpath(remote_name)
            logger.info("uploding [%s] => [%s]", fp, remote_name)
            conn.upload(remote_name, f)
