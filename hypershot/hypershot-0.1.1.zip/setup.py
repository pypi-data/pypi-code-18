#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create screen shots of a video file, and upload them to an image host.

See the `GitLab project page`_ for usage documentation and installation instructions.

| Copyright (c) 2017 Kybernetics Project · MIT licensed

.. _`GitLab project page`: https://gitlab.com/kybernetics/hypershot#hypershot
"""
import io
import os
import re

from setuptools import setup, find_packages

version = None
rootdir = os.path.dirname(__file__)
with io.open(os.path.join(rootdir, 'src/hypershot/__init__.py'), encoding='utf-8') as pkg_init:
    for line in pkg_init:
        matched = re.match(r"^__version__ = '([.0-9]+)'", line)
        if matched:
            version = matched.group(1)

assert version, "Bad or missing version in package __init__!"

short_desc, long_desc = __doc__.strip().split('.', 1)
pkg_info = dict(
    name='hypershot',
    version=version,
    author='Automan',
    author_email='automan@protonmail.ch',
    url='https://gitlab.com/kybernetics/hypershot',
    description=short_desc + '.',
    long_description=long_desc.strip(),
    license='MIT',
    classifiers=[  # http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Multimedia :: Video',
    ],
    keywords='screenshot mplayer ffmpeg'.split(),
    install_requires=[re.split('[=<>,]', x)[0]
        for x in open('requirements.txt')
        if x.strip() and x[0] not in '-#'
    ],
    package_dir = {"": "src"},
    packages = find_packages("src", exclude = ["tests"]),
    data_files = [
        ("EGG-INFO", [
            "README.md", "LICENSE",
        ]),
    ],
    entry_points = {
        "console_scripts": [
            "hypershot = hypershot.cli:run",
        ],
    },
    include_package_data = True,
    zip_safe = True,
)

if __name__ == '__main__':
    setup(**pkg_info)
