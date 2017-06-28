"""Various number types for Python"""

from . import typed_complex, coordinates

from .typed_complex import *
from .coordinates import *

__all__ = ['typed_complex']

__all__.extend(typed_complex.__all__)
__all__.extend(coordinates.__all__)

__all__ = tuple(__all__)

__author__ = 'Mital Ashok'
__credits__ = ['Mital Ashok']
__license__ = 'MIT'
__version__ = '0.0.2'
__maintainer__ = 'Mital Ashok'
__author_email__ = __email__ = 'mital.vaja[AT]googlemail.com'
__status__ = 'Development'
