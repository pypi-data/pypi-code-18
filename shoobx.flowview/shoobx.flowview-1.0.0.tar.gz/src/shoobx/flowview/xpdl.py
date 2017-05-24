###############################################################################
#
# Copyright 2014 by Shoobx, Inc.
#
###############################################################################
import logging
import pkg_resources

from lxml import etree

log = logging.getLogger(__name__)


class ResourceResolver(etree.Resolver):
    prefix = "flowview:"

    def resolve(self, url, pubid, context):
        if url.startswith(self.prefix):
            fn = url[len(self.prefix):]
            log.debug("Resolving resource %s", fn)

            res = pkg_resources.resource_stream("shoobx.flowview", fn)
            return self.resolve_file(res, context)


def transform_to_html(xpdl_filename):
    """Transform given XPDL file to HTML
    """
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())

    template = pkg_resources.resource_stream("shoobx.flowview", "xpdl.xslt")
    dom = etree.parse(xpdl_filename)
    xslt = etree.parse(template, parser)
    template.close()
    transform = etree.XSLT(xslt)
    htmldom = transform(dom)
    # html = etree.tostring(htmldom, pretty_print=True)
    html = str(htmldom)
    return "<!DOCTYPE html>\n" + html
