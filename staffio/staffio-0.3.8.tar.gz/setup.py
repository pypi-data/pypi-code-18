#!/usr/bin/env python

from setuptools import setup

description = """
A client of StaffIO (An OAuth2 Provider) with python,
Supported:
- Flask
- Sentry Social Auth (Django)
"""

setup(
    name="staffio",
    version="0.3.8",
    url='https://github.com/liut/staffio-py',
    license='',
    description=description,
    author='Eagle Liut',
    packages=['flask_staffio', 'django_staffio'],
    keywords=['db', 'auth', 'staffio'],
    install_requires=[
        'future'
    ],
    extras_require={
        'flask': [
            'Flask',
            'Flask-OAuthlib>=0.9.3',
        ],
        'django': ['Django>=1.6.0'],
        'sentry': ['sentry>=8.0', 'oauth2'],
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
