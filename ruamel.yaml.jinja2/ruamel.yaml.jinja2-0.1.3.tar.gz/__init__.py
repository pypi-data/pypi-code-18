# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.yaml.jinja2',
    version_info=(0, 1, 3),
    __version__='0.1.3',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='jinja2 pre and post-processor to update with YAML',
    # keywords="",
    entry_points=None,
    # entry_points=None,
    license='MIT',
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    keywords='yaml 1.2 parser round-trip jinja2',
    nested=True,
    install_requires=['ruamel.yaml'],
    tox=dict(
        env='23',
    ),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
