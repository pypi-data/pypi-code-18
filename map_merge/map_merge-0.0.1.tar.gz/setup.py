"""
    map_merge
    ~~~~~~~~~

    Merge Python mapping instances.

    :copyright: (c) 2017 Andrew Hawker.
    :license: Apache 2.0, see LICENSE file.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='map_merge',
    version='0.0.1',
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/map_merge',
    license='Apache 2.0',
    description='Merge Python mapping instances',
    long_description=__doc__,
    py_modules=['map_merge'],
    install_requires=['six'],
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
