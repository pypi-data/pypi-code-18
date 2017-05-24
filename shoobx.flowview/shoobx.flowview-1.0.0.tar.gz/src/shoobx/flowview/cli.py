###############################################################################
#
# Copyright 2014 by Shoobx, Inc.
#
###############################################################################
import argparse
import logging
import pkg_resources

from shoobx.flowview import xpdl


log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description='Shoobx Flowview: XPDL Viewer')
parser.add_argument("xpdl", help="Input XPDL filename")
parser.add_argument("html", help="Output HTML filename")


def setup_logging(args):
    logging.basicConfig(level=logging.INFO)


def get_version():
    dist = pkg_resources.get_distribution("shoobx.flowview")
    return dist.version


def main():
    args = parser.parse_args()
    setup_logging(args)
    log.info("Shoobx Flowview %s" % get_version())

    html = xpdl.transform_to_html(args.xpdl)

    with (open(args.html, "w")) as f:
        f.write(html)

    log.info("Transform completed.")