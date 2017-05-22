from pyquery import PyQuery as _pq
from bs4 import BeautifulSoup as _BS
from lxml.etree import  XMLSyntaxError

class pq:


    def __init__(self, *args, **kargs):
        self.encoding = 'utf8'
        if 'encoding' in kargs:
            self.encoding = kargs['encoding']

        try:
            self._raw = _pq(*args, **kargs)
            self.handler = 'pq'
        except XMLSyntaxError as e:
            self._raw = _BS(*args, features='lxml',**kargs)
            self.handler = 'bs'
    
    def __repr__(self):
        return self._raw.__repr__()

    def __call__(self, st):
        if self.handler =='pq':
            return self._raw(st).decode(self.encoding)
        elif self.handler == 'bs':
            return self._raw.select(st)

    def html(self, encoding='utf8'):
        if self.handler =='pq':
            return self._raw.html()
        elif self.handler == 'bs':
            return self._raw.decode(eventual_encoding=encoding)



    # def attr(self):
