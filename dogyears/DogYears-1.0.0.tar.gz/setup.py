#!/usr/bin/env python
import ssl
from distutils.core import setup

ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='DogYears',
    version='1.0.0',
    packages=['dogyear'],
    url='https://github.com/Code-ReaQtor/DogYears',
    download_url='https://github.com/Code-ReaQtor/DogYears/archive/1.0.1.tar.gz',
    license='MIT',
    author='Ronie Martinez',
    author_email='ronmarti18@gmail.com',
    description='Convert human years to dog years and vice versa.',
    install_requires=['numpy==1.12.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
