from pyquery import PyQuery as _pq
from bs4 import BeautifulSoup as _BS
from lxml.etree import  XMLSyntaxError

class XmlParser:


    def __init__(self, *args, **kargs):
        self.encoding = 'utf8'
        self._text = None
        if 'encoding' in kargs:
            self.encoding = kargs['encoding']

        try:
            self._raw = _pq(*args, **kargs)
            self.handler = 'pq'
        except XMLSyntaxError as e:
            self._raw = _BS(*args, features='lxml',**kargs)
            self.handler = 'bs'
    
    def __repr__(self):
        if self.handler == "bs":
            return self._raw.select("title").string
        return self._raw("title").text()
        

    def __call__(self, st):
        if self.handler =='pq':
            return self._raw(st)
        elif self.handler == 'bs':
            return self._raw.select(st)

    def html(self, encoding='utf8'):
        if self.handler =='pq':
            return self._raw.html()
        elif self.handler == 'bs':
            return self._raw.decode(eventual_encoding=encoding)

    def text(self):
        if self.handler == "bs":
            pp = _pq(self.html())
            pp("script").remove()
            pp("style").remove()
            return pp.text()
        else:
            self._raw("script").remove()
            self._raw("style").remove()
            return self._raw.text()

    # def attr(self):
