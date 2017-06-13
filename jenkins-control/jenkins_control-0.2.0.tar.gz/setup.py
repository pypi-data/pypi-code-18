#!/bin/env python
"""
Setuptools file for jenkins_control
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='jenkins_control',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/marhag87/jenkins_control',
    version='0.2.0',
    packages=find_packages(),
    license='WTFPL',
    description='Simple controls for jenkins',
    long_description='Simple controls for jenkins, intended for use with tmux and similar',
    install_requires=[
        'requests',
        'pyyamlconfig',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    scripts=['bin/jc'],
)
