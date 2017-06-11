__version__ = '1.0.3'
#从本文件夹里import models.py和exceptions.py
#from . import models, exceptions
from . import osskey
#从本目录下api.py里import Service和Bucket这个类
#from .api import Service, Bucket
from .osskey import osskey
