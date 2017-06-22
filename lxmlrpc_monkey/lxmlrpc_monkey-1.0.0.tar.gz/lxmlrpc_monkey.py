# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'Dmytro Katyukha'

# Enable LXML parser for xmlrpc if possible,
# it will strongly reduce memory usage for large data sets
# for python2.7
# --------------------------------------------------------
from lxml.etree import XMLPullParser


class LXMLParser(object):
    def __init__(self, target):
        self._parser = XMLPullParser(events=('start', 'end'),
                                        huge_tree=True)
        self._target = target

    def handle_events(self):
        for action, element in self._parser.read_events():
            if action == 'start':
                self._target.start(element.tag, element.attrib)
            elif action == 'end':
                if element.text:
                    self._target.data(element.text)
                self._target.end(element.tag)
                element.clear()

    def feed(self, data):
        try:
            self._parser.feed(data)
        except:
            raise
        self.handle_events()

    def close(self):
        self._parser.close()



def patch_xmlrpclib():
    """ Patch xmlrpclib to make it use *lxml* based parser
        This reduces memory usage for for big datasets (100+ Mb)
    """
    import xmlrpclib

    def _wrap_xmlrpclib(name):
        """ Simple decorator, that replaces xmlrpclib's object
            with decorated one
        """
        def decorator(obj):
            obj.__old_xmlrpclib_obj__ = getattr(xmlrpclib, name, None)
            setattr(xmlrpclib, name, obj)
            return obj
        return decorator

    # Override xmlrpclib._decode to avoid decoding unicode
    @_wrap_xmlrpclib('_decode')
    def _decode(data, encoding, *args, **kwargs):
        if isinstance(data, unicode):
            return data
        return _decode.__old_xmlrpclib_obj__(data, encoding, *args, **kwargs)


    # Override xmlrpclib._stringify to encoding string to plain ascii
    # it eats a lot of memory on a very long strings
    @_wrap_xmlrpclib('_stringify')
    def _stringify(string):
        return string


    # Set default parser for xmlrpclib
    @_wrap_xmlrpclib('getparser')
    def _getparser(use_datetime=0):
        """getparser() -> parser, unmarshaller
        Create an instance of the fastest available parser, and attach it
        to an unmarshalling object.  Return both objects.
        """
        target = xmlrpclib.Unmarshaller(use_datetime=use_datetime)
        parser = LXMLParser(target)
        return parser, target
