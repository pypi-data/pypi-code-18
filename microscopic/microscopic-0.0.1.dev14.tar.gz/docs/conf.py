#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# microscopic documentation build configuration file

import alabaster

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'alabaster',
    'sphinxcontrib_trio'
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# general project information
project = 'microscopic'
copyright = '2017, Zack Buhman'
#version = microscopic.__version__
#release = microscopic.__version__

# styles
pygments_style = 'sphinx'
highlight_language = 'python3'

# The theme to use for HTML and HTML Help pages.
html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]

html_theme_options = {
    'description': 'over-engineered concurrent tiny-url generator',
    'github_user': 'buhman',
    'github_repo': 'microscopic',
    'github_button': True,
    'github_type': 'star',
    'github_banner': True,
    'shield_list': [
        {
            'image': 'https://img.shields.io/circleci/project/github/buhman/microscopic.svg',
            'target': 'https://circleci.com/gh/buhman/microscopic'
        },
        {
            'image': 'https://img.shields.io/codecov/c/github/buhman/microscopic.svg',
            'target': 'https://codecov.io/gh/buhman/microscopic'
        },
        {
            'image': 'https://img.shields.io/pypi/v/microscopic.svg',
            'target': 'https://pypi.org/project/microscopic/'
        }
    ]
}

html_sidebars = {
    '**': [
        'about.html', 'navigation.html', 'searchbox.html',
    ]
}
