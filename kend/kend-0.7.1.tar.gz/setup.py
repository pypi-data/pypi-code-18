import os
from setuptools import setup, find_packages

requires = [
    'lxml',
]

setup(
    name='kend',
    version='0.7.1',
    description='Client package for interacting with the Utopia kend server',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],
    author='David Thorne',
    author_email='davethorne@gmail.com',
    license='GPLv3+',
    packages=find_packages(),
    install_requires=requires,
    tests_require=requires,
    test_suite='kend',
)

