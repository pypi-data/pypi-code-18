from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

VERSION = 1.0

setup(
    name='Streamy',
    version=VERSION,
    description=('Streamy lets you stream Json as a generator'),
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url='http://github.com/timedata-org/streamy/',
    download_url='http://github.com/timedata-org/streamy/archive/1.0.tar.gz',
    license='MIT',
    packages=find_packages(exclude=['test']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=['pytest'],
    keywords=['git', 'import'],
    include_package_data=True,
    install_requires=['GitPython', 'requests'],
)
