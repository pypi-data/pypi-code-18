# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

_package_data = dict(
    full_package_name='ruamel.dcw',
    version_info=(0, 5, 0),
    __version__='0.5.0',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='docker-compose wrapper allowing for user data and env. var defaults',
    # keywords="",
    entry_points='dcw=ruamel.dcw.__main__:main',
    # entry_points=None,
    license='MIT',
    since=2016,
    # status: "α|β|stable",  # the package status on PyPI
    data_files=['_templates/systemd', '_templates/upstart'],
    universal=True,
    install_requires=dict(
        any=[
            'docker-compose>=1.8.0,<1.9.0',
            'ruamel.yaml>=0.11',
            'ruamel.std.pathlib',
            'ruamel.showoutput',
        ],
    ),
)

# "python-daemon",

version_info = _package_data['version_info']
__version__ = _package_data['__version__']
