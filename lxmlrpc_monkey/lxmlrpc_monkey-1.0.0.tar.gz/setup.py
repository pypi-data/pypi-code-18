#!/usr/bin/env python
from setuptools import setup

_doc = open('README.rst', 'rt').read()

setup(
    name='lxmlrpc_monkey',
    version='1.0.0',
    description='xmlrpclib patch to reduce its memory consumption',
    author='Dmytro Katyukha',
    author_email='firemage.dima@gmail.com',
    url='https://github.com/katyukha/lxmlrpc_monkey',
    long_description=_doc,
    install_requires=[
        'lxml',
    ],
    license="GPL",
    py_modules=['lxmlrpc_monkey'],
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['xmlrpc', 'xmlrpclib'],
)
