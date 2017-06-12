#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import shutil
import sys
import os

project_root = os.path.dirname(os.path.dirname(__file__))

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)

import roundhouse
from sphinx.apidoc import main

apidoc_dir = './apidoc'
if os.path.isdir(apidoc_dir):
    shutil.rmtree(apidoc_dir)

main(['-f', '-T', '-e', '-M', '-o', apidoc_dir, '../roundhouse'])

# -- General configuration ---------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Roundhouse'
copyright = u"{}, {}".format(datetime.datetime.now().year, project)

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The full version, including alpha/beta/rc tags.
release = roundhouse.__version__
# The short X.Y version.
version = '.'.join(release.split('.')[:2])

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'show_powered_by': False,
    'description': roundhouse.__doc__
}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as
# html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the
# top of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon
# of the docs.  This file should be a Windows icon file (.ico) being
# 16x16 or 32x32 pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names
# to template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer.
# Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer.
# Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages
# will contain a <link> tag referring to it.  The value of this option
# must be the base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'roundhousedoc'


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index', 'roundhouse.tex',
     u'Roundhouse Documentation',
     u'Nick Allen', 'manual'),
]

# The name of an image file (relative to this directory) to place at
# the top of the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings
# are parts, not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'roundhouse',
     u'Roundhouse Documentation',
     [u'Nick Allen'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'roundhouse',
     u'Roundhouse Documentation',
     u'Nick Allen',
     'roundhouse',
     'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# -- Options for extra plugins ----------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None)
}
