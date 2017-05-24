import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'pub_requests.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]

__version__ = version_line.split('__version__ = ')[-1][1:][:-2]
print(__version__)

setuptools.setup(
    name="pub_requests",
    version=__version__,
    url="http://git.internal.lucidmarkets.com/aashiqd/pub_requests",

    author="Aashiq Dheeraj",
    author_email="aashiq.dheeraj@lucidmarkets.com",

    description="Utils for querying ME2_PUB",
    long_description=open('README.rst').read(),

    py_modules=['pub_requests'],
    zip_safe=False,
    platforms='any',

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
