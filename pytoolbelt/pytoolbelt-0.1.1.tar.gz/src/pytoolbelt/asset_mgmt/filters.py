# -*- coding: utf-8 -*-
"""

"""

import StringIO
import collections, logging, os, re

log = logging.getLogger(__name__)

class Filter(object):
    def validate(self):
        raise Exception(u"nothing implemented here")

# Image Type / File type filters
class Jpeg(Filter):
    pass

class Gif(Filter):
    pass

class Png(Filter):
    pass

class Resize(Filter):
    def __init__(self, width, heighjt):
        pass

class Watermark(Filter):
    def __init__(self, image_stream):
        pass

class Pdf(Filter):
    pass

class Zip(Filter):
    pass

class Images(Filter):
    pass