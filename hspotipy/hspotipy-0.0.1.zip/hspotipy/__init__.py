"""
Spotify API
"""
from __future__ import absolute_import


try:
    install_instr = "Please make sure you install a recent enough version of spotipy."
    import spotipy
except ImportError:
    raise ImportError("__init__.py : Could not import spotipy." + install_instr)

from . import user


__version__ = "0.0.1"

global_flag = {}
global_dict = {}

# create your application, https://developer.spotify.com/my-applications/
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
