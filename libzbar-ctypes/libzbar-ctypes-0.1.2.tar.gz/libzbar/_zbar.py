# by jf
# zaazbb <zaazbb@163.com>
# https://github.com/zaazbb/zbar_ctypes

from ctypes import *


_libzbar = CDLL('libzbar.so.0')


# symbol.

class zbar_symbol(Structure):
    _fields_ = []
zbar_symbol_next = _libzbar.zbar_symbol_next
zbar_symbol_next.restype = POINTER(zbar_symbol)
zbar_symbol_next.argtypes = [POINTER(zbar_symbol)]

zbar_symbol_get_type = _libzbar.zbar_symbol_get_type
zbar_symbol_get_type.restype = c_int
zbar_symbol_get_type.argtypes = [POINTER(zbar_symbol)]

zbar_symbol_get_data = _libzbar.zbar_symbol_get_data
zbar_symbol_get_data.restype = c_char_p
zbar_symbol_get_data.argtypes = [POINTER(zbar_symbol)]

zbar_get_symbol_name = _libzbar.zbar_get_symbol_name
zbar_get_symbol_name.restype = c_char_p
zbar_get_symbol_name.argtypes = [c_int]

#symbolset
class zbar_symbol_set(Structure):
    _fields_ = []

zbar_symbol_set_get_size = _libzbar.zbar_symbol_set_get_size
zbar_symbol_set_get_size.restype = c_int
zbar_symbol_set_get_size.argtype = [POINTER(zbar_symbol_set)]

# image.
    
class zbar_image(Structure):
    _fields_ = []
    
zbar_image_create = _libzbar.zbar_image_create
zbar_image_create.restype = POINTER(zbar_image)
zbar_image_create.argtypes = []

zbar_image_destroy = _libzbar.zbar_image_destroy
zbar_image_destroy.restype = None
zbar_image_destroy.argtypes = [POINTER(zbar_image)]

##zbar_image_get_data = _libzbar.zbar_image_get_data
##zbar_image_get_data.restype = c_void_p
##zbar_image_get_data.argtypes = [POINTER(zbar_image)]

zbar_image_set_size = _libzbar.zbar_image_set_size
zbar_image_set_size.restype = None
zbar_image_set_size.argtypes = [POINTER(zbar_image), c_uint, c_uint]

zbar_image_set_format = _libzbar.zbar_image_set_format
zbar_image_set_format.restype = None
zbar_image_set_format.argtypes = [POINTER(zbar_image), c_ulong]

##zbar_image_free_data = _libzbar.zbar_image_free_data
##zbar_image_free_data.restype = None
##zbar_image_free_data.argtypes = [POINTER(zbar_image)]

zbar_image_set_data = _libzbar.zbar_image_set_data
zbar_image_set_data.restype = None
zbar_image_set_data.argtypes = [POINTER(zbar_image),
                                c_void_p, c_ulong, c_void_p]


zbar_image_first_symbol = _libzbar.zbar_image_first_symbol
zbar_image_first_symbol.restype = POINTER(zbar_symbol)
zbar_image_first_symbol.argtypes = [POINTER(zbar_image)]

zbar_image_get_symbols = _libzbar.zbar_image_get_symbols
zbar_image_get_symbols.restype = POINTER(zbar_symbol_set)
zbar_image_get_symbols.argtypes =[POINTER(zbar_image)]


# image scanner.

class zbar_image_scanner(Structure):
    _fields_ = []
    
zbar_image_scanner_create = _libzbar.zbar_image_scanner_create
zbar_image_scanner_create.restype = POINTER(zbar_image_scanner)
zbar_image_scanner_create.argtypes = []

zbar_image_scanner_destroy = _libzbar.zbar_image_scanner_destroy
zbar_image_scanner_destroy.restype = None
zbar_image_scanner_destroy.argtypes = [POINTER(zbar_image_scanner)]

zbar_image_scanner_set_config = _libzbar.zbar_image_scanner_set_config
zbar_image_scanner_set_config.restype = c_int
zbar_image_scanner_set_config.argtypes = [POINTER(zbar_image_scanner),
                                          c_int, c_int, c_int]

zbar_parse_config = _libzbar.zbar_parse_config
zbar_parse_config.restype = c_int
zbar_parse_config.argtypes = [
    c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

# no support in libzbar0.
##zbar_image_scanner_parse_config = _libzbar.zbar_image_scanner_parse_config
##zbar_image_scanner_parse_config.restype = c_int
##zbar_image_scanner_parse_config.argtypes = [
##    POINTER(zbar_image_scanner), c_char_p]

zbar_scan_image = _libzbar.zbar_scan_image
zbar_scan_image.restype = c_int
zbar_scan_image.argtypes = [POINTER(zbar_image_scanner), POINTER(zbar_image)]


