# -*- coding: utf-8 -*-
#
# xml2dict/xml2dict.py
#
# See MIT License file.
#
"""
Convert XML to a Python dict.

"""
__docformat__ = "restructuredtext en"


import io
import re
import six
import logging
import defusedxml.ElementTree as ET


class XML2Dict(object):
    __NSPACE_REGEX = r"^\{(?P<uri>.*)\}(?P<tag>.*)$"
    __NSPACE_OBJ = re.compile(__NSPACE_REGEX)

    def __init__(self, empty_tags=True, rm_whitespace=True, logger_name='',
                 level=None):
        if logger_name == '':
            logging.basicConfig()

        self._log = logging.getLogger(logger_name)

        if level:
            self._log.setLevel(level)

        self.__namespaces = {}
        self.__empty_tags = empty_tags
        self.__rm_whitespace = rm_whitespace

    def _set_file_object(self, xml):
        if isinstance(xml, io.IOBase):
            xml.seek(0) # Make sure we're at the start of the file.
            self._xml = xml
        else:
            self._xml = six.StringIO(xml)

    def parse(self, xml, encoding=None):
        data = []
        parser = ET.DefusedXMLParser(encoding=encoding)
        self._set_file_object(xml)

        try:
            tree = ET.parse(self._xml, parser=parser, forbid_dtd=True)
            root = tree.getroot()
            self.__namespaces.update(dict([(v,k) for k,v in root.items()]))
            self.__node(data, root)
        except ET.ParseError as e:
            self._log.error("Could not parse xml, %s", e)
            raise e

        self._log.debug("data: %s", data)
        return data

    def __node(self, data, node):
        child_data = {}
        data.append(child_data)
        # Process tag
        tag_name = node.tag
        nspace, name = self.__split_namespace(tag_name)
        ns_tag = "{}{}{}".format(nspace, ':' if nspace else '', name)
        text = self.value_hook(node.text)
        child_data['attrib'] = {k: self.value_hook(v)
                                for k,v in node.attrib.items()}
        child_data['tag'] = {'nspace': nspace,
                             'tag': name,
                             'value': self.__tag_value(text)}
        children_data = []
        child_data['children'] = children_data

        for child in node.getchildren():
            self.__node(children_data, child)

    def __split_namespace(self, tag):
        sre = self.__NSPACE_OBJ.search(tag)

        if sre:
            nspace = sre.group('uri')
            nspace = self.__namespaces.get(nspace, '')
            name = sre.group('tag')
        else:
            nspace = ''
            name = tag

        return nspace, name

    def __tag_value(self, text):
        if text:
            if self.__rm_whitespace:
                text = text.strip()
        elif self.__empty_tags:
            text = ''

        return text

    def value_hook(self, value):
        """
        This hook can be overridden to convert values to Python types.
        """
        return value

def _openFile(filePath, how='rb'):
    fp = None

    try:
        fp = open(filePath, how)
    except IOError as e:
        msg = "Error: Could not open file: {}, {}."
        raise IOError(msg.format(filePath, e))

    return fp


if __name__ == '__main__':
    import sys, traceback
    from pprint import pprint

    # encoding="utf-8"
    data = '''<?xml version="1.0" standalone="yes" ?>
<response status="ok">
  <user name="example.gen"
        type="Generic"
        descr="Example User"
        homedirectory=""
        homedrive=""
        loginscript=""
        profilepath=""
        loginshell=""
        unixhomedirectory=""
        env="dev.example.com"
        status="enabled"
        passwordexpires="2015-10-21T21:16:14Z"
        passwordlastset="2015-04-24T21:16:14Z"
        dn="CN=test-root.gen,OU=Generics,OU=Example Users,DC=dev,DC=example,DC=com"
        upn="test-root.gen@dev.example.com"
        url="https://ds-api.example.com/DS/v1/dev.example.com/User/test-root.gen">
    <env-list count="2">
      <env>dev.example.com</env>
      <env>dsxdev.example.com</env>
    </env-list>
    <owner-list count="2">
      <owner>joeblow</owner>
      <owner>jhamilton</owner>
    </owner-list>
  </user>
</response>
'''

    try:
        if len(sys.argv) > 1:
            xml = _openFile(sys.argv[1])
        else:
            xml = data

        x2d = XML2Dict(level=logging.DEBUG)
        out = x2d.parse(xml)
        print("\nResults:")
        pprint(out)
    except:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}\n".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)
