# coding:utf-8

import sys

try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

setup(
    name='zkSync',
    version='0.1.1',
    description='Copy zk data from one node to another node',
    keywords='zookeeper sync zk zkSync',
    author='dvsv2',
    author_email='dvsv2@foxmail.com',
    url='',
    entry_points={
        'console_scripts': [
        'zkSync = execdir.zkSync:main',
    ],
},
    packages=['execdir'],
    include_package_data=True,
    install_requires=['kazoo', 'logging']
)
