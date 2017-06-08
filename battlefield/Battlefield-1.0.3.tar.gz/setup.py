# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Battlefield',
    version='1.0.3',
    packages=find_packages(),
    install_requires=['pika'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='robot game battlefield',
    url='https://github.com/tehpug/Battlefield',
    license='GPLv3',
    author='Mehdy Khoshnoody',
    author_email='mehdy.khoshnoody@gmail.com',
    description='Utilities to create games and robots for Battlefield')
