# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-auth-email',
    version='0.0.1a5',
    author='Konstantin Kruglov',
    author_email='kruglovk@gmail.com',
    description='Authentication using email only',
    url='https://github.com/k0st1an/django-auth-email',
    packages=find_packages(),
    license='Apache License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.9'
    ],
)
