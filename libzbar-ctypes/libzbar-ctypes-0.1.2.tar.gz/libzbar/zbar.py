# by jf
# zaazbb <zaazbb@163.com>
# https://bitbucket.org/zaazbb/zbar_ctypes

import collections

from ._zbar import *


class Config:
    ENABLE = 0

    
class Symbol:
    NONE = 0
    QRCODE = 64
    def __init__(self, symbol):
        self._symbol = symbol
        self._data = None
        self._type = None
        self._name = None

    def _get_data(self):
        if not self._data:
            self._data = zbar_symbol_get_data(self._symbol)
        return self._data

    def _get_type(self):
        if not self._type:
            self._type = zbar_symbol_get_type(self._symbol)
        return self._type

    def _get_name(self):
        if not self._name:
            self._name = zbar_get_symbol_name(self._get_type())
        return self._name

    data = property(_get_data)
    type = property(_get_type)
    name = property(_get_name)
    
class SymbolSet:
    def __init__(self, symbolset):
        self._symbolset = symbolset
        self._size = 0

    def _get_size(self):
        self._size = zbar_symbol_set_get_size(self._symbolset)
        return self._size 

    size = property(_get_size)

# image formats.
# 'GREY', 'Y800', 'Y8  ', 'Y8\x00\x00'
# 'YUV9', 'YVU9'
# 'I420', 'YU12', 'YV12', '411P'
# 'NV12', 'NV21'
# '422P'
# 'YUYV', 'YUY2', 'YVYU', 'UYVY'
# 'RGB3', 'BGR3', '\x03\x00\x00\x00', 'RGB4', 'BGR4', 'RGBP', 'RGBO',
# 'RGBR', 'RGBQ'

class Image:
    def __init__(self, width, height, format_, data):
        self._image = zbar_image_create()
        zbar_image_set_size(self._image, width, height)
        if len(format_) == 4:
            try:
                formatcode = int.from_bytes(format_.encode(), 'little')
            except:
                import array
                formatcode = array.array('L', format_)[0]
            zbar_image_set_format(self._image, formatcode)
        self._data = data
        zbar_image_set_data(self._image, data, len(data), None)

        self._cursym = None
        
    def __del__(self):
        if self._image:
            zbar_image_destroy(self._image)
        del self._data

    def __iter__(self):
        return self

    def __next__(self):
        if self._cursym:
            self._cursym = zbar_symbol_next(self._cursym)
        else:
            self._cursym = zbar_image_first_symbol(self._image)
        if self._cursym:
            return Symbol(self._cursym)
        else:
            raise StopIteration

    def next(self):
        return self.__next__()
        
    def get_symbols(self):
        return SymbolSet(zbar_image_get_symbols(self._image))
    
class ImageScanner:
    def __init__(self):
        self._scanner = zbar_image_scanner_create()

    def __del__(self):
        if self._scanner:
            zbar_image_scanner_destroy(self._scanner)

    def set_config(self, symbol_type, config, value):
        return zbar_image_scanner_set_config(self._scanner,
                                             symbol_type, config, value)

    def parse_config(self, config_string):
        sym = c_int()
        cfg = c_int()
        val = c_int()
        return zbar_parse_config(
            cast(config_string, c_char_p),
            byref(sym),byref(cfg), byref(val)) \
                or zbar_image_scanner_set_config(self._scanner, sym, cfg, val)

    def scan(self, image):
        return zbar_scan_image(self._scanner, image._image)

