import sys


def is_python_3():
    return sys.version_info[0] is 3

try:
    if is_python_3():
        import tkinter
    else:
        import Tkinter
except ImportError as e:
    print("ttkthemes could not be imported because tkinter is not available")
    print("If you are running Linux, make sure that the package python-tk is installed")
    print("If you are running Windows, make sure you re-install Python with the tkinter option selected")
    raise e

from ttkthemes.themed_tk import ThemedTk
