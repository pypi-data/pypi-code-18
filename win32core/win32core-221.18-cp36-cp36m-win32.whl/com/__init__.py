import os

from . import gen_py
from _win32com import *
from _win32com import _univgw
from tempfile import gettempdir

__gen_path__ = os.path.join(gettempdir(), 'pywin32', 'gen_py')
gen_py.__path__.insert(0, __gen_path__)