# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

dependencies = ['click']

with open('README.md') as r:
    long_description = r.read()

with open('LICENSE') as l:
    license = l.read()

setup(
    name = 'minicss',
    packages = ['minicss'],
    version = '1.0',
    description = long_description,
    long_description = long_description,
    author = 'Yochem van Rosmalen',
    author_email = 'yochem@icloud.com',
    url = 'https://github.com/yochem/minicss',
    download_url = 'https://www.github.com/yochem/minicss/archive/1.0.tar.gz',
    license = license,
    include_package_data = True,
    zip_safe = False,
    platforms = 'any',
    install_requires = dependencies,
    entry_points = {
        'console_scripts': [
            'mini=minicss.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
