"""
libknot setup module.
"""

from setuptools import setup, find_packages

setup(
    name='libknot',
    version='2.5.2',
    description='Python bindings for libknot',
    url='https://github.com/CZ-NIC/knot',
    author='Andre Keller',
    author_email='andre.keller@vshn.ch',
    license='GPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=[
        'libknot',
    ]

)
