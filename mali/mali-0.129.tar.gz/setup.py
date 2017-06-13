# coding=utf-8
import os
from setuptools import setup, find_packages

build = os.environ['PIP_BUILD']
keywords = os.environ['PIP_KEYWORDS']


version = '0.{}'.format(build)

with open('requirements.txt') as f:
    install_requires = [r for r in f.readlines() if len(r.strip()) > 0]

setup(
    name='mali',
    version=version,
    description='Command line to for missinglink.ai platform',
    author='missinglink.ai',
    author_email='support+mali@missinglink.ai',
    url='https://missinglink.ai',
    license='Apache',
    py_modules=['mali'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        mali=mali:cli
    ''',
)
