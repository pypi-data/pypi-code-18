# -*- coding: utf-8 -*-
r"""
.. _my_label:

=========================
Test supported docstrings
=========================

helo
"""
# Author: Óscar Nájera
# License: 3-clause BSD


from __future__ import division, absolute_import, print_function
import os
import re
from docutils.core import publish_string, publish_programmatically
from sphinx_gallery import gen_rst as sg
from sphinx.application import Sphinx

cwd = os.getcwd()
doc, _ = sg.get_docstring_and_rest(__file__)
# doc, _ =
# sg.get_docstring_and_rest("/home/oscar/dev/sphinx-gallery/examples/plot_colors.py")

docstr = publish_string(doc, writer_name='xml')

re.search("<title>(.+)</title>", docstr.decode('utf-8'))
first = re.search("<paragraph>(.+?)</paragraph>",
                  docstr.decode('utf-8'), flags=re.DOTALL)
# re.sub("\n", " ", first.group(1))
sg.extract_intro("/home/oscar/dev/sphinx-gallery/examples/plot_colors.py")

import docutils
parser = docutils.parsers.rst.Parser()
document = docutils.utils.new_document("file",
                                       settings=docutils.frontend.OptionParser(
                                           components=(docutils.parsers.rst.Parser,)).get_default_values())
parser.parse(doc, document)


class LinkCheckerVisitor(docutils.nodes.GenericNodeVisitor):

    paragraphs = []
    title = ""

    def visit_paragraph(self, node):
        self.paragraphs.append(node.astext())

    def visit_title(self, node):
        self.title = node.astext()

    def default_visit(self, node):
        pass


visitor = LinkCheckerVisitor(document)
ao = document.walk(visitor)
wa = visitor.paragraphs[0]
