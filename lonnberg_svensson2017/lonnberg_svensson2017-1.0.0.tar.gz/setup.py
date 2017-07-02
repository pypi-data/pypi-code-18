#!/usr/bin/env python

from setuptools import setup

version = '1.0.0'

required = open('requirements.txt').read().split('\n')

setup(
    name='lonnberg_svensson2017',
    version=version,
    description='Expression data for Lönnberg + Svensson et al, "Single-cell RNA-seq and computational analysis using temporal mixture modelling resolves Th1/Tfh fate bifurcation in malaria," Science Immunology (2017)',
    author='Olga Botvinnik',
    author_email='olga.botvinnik@gmail.com',
    url='https://github.com/olgabot/lonnberg_svensson2017',
    packages=['lonnberg_svensson2017'],
    install_requires=required,
    long_description='See ' + 'https://github.com/olgabot/lonnberg_svensson2017',
    license='MIT'
)
