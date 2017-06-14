# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.yaml.jinja2',
    version_info=(0, 1, 1),
    __version__='0.1.1',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='jinja2 pre and post-processor to update with YAML',
    # keywords="",
    entry_points='jinja2=ruamel.yaml.jinja2.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2017',
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    nested=True,
    install_requires=dict(
        any=[],
    ),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
