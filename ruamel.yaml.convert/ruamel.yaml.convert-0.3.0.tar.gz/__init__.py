# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

# install_requires of ruamel.base is not really required but the old
# ruamel.base installed __init__.py, and thus a new version should
# be installed at some point

_package_data = dict(
    full_package_name='ruamel.yaml.convert',
    version_info=(0, 3, 0),
    __version__='0.3.0',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='data format conversion routines to/from YAML',
    entry_points=None,
    install_requires=['ruamel.yaml', 'python-dateutil'],
    extras_require={'all': ['python-dateutil', 'beautifulsoup4'], 'csv': ['python-dateutil'], 'html': ['beautifulsoup4']},  # NOQA
    since=2015,
    nested=True,
    status=u'α',
    universal=True,
    tox=dict(
        env='23',
        deps=['python-dateutil', 'beautifulsoup4'],
    ),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

from .syncjson import *    # NOQA
