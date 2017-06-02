from .ocean import Ocean, main, get_ocean
import os

__main__ = main
try:
    __version__ = open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read()
except BaseException:
    __version__ = "N/A"
__all__ = ('Ocean', 'get_ocean', '__version__', '__main__')
