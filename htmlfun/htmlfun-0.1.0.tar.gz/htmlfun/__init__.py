# -*- coding: utf-8 -*-

"""

htmlfun.py
Helper functions for generating HTML documents.

Usage:

    >>> from htmlfun.elements import html, body, h1
    >>> from htmlfun import build_doc

    >>> content = body(h1({"class": "header"}, "Hello, world!"))
    >>> doc = build_doc(content)
    >>> print(doc)

HTML elements are represented as nested lists of strings. These lists
can be flattened using the flatten() core function and joined together
into an html document. The build_doc() helper function is a wrapper
around flatten() that wraps your tags in an HTML5 declaration and a
root <html> tag pair.

"""


__title__ = 'htmlfun'
__version__ = "0.1.0"
__author__ = 'Nick Lamberth'
__license__ = 'MIT'


from .core import *
from . import elements
