# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

PACKAGE_NAME = 'tlscanary'
PACKAGE_VERSION = '3.1.0a5'

INSTALL_REQUIRES = [
    'coloredlogs',
    'cryptography',
    'ipython',
    'worq'
]

TESTS_REQUIRE =[
    'nose',
    'mock'
]

DEV_REQUIRES = TESTS_REQUIRE

PACKAGE_DATA = {
    'tlscanary': [
        'default_profile/*',
        'js/*',
        'sources/*.csv',
        'template/*',
        'template/*/*',
        'template/*/*/*',
        'template/*/*/*/*'
    ]
}

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='TLS/SSL Test Suite for Firefox',
    long_description='TLS Canary is a testing tool for Mozilla Firefox that queries a large '
                     'set of HTTPS-enabled web servers to spot regressions and performance '
                     'issues in the browser\'s TLS stack.',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing'
    ],
    keywords=['mozilla', 'firefox', 'tls', 'regression-testing', 'testing'],
    author='Christiane Ruetten',
    author_email='cr@mozilla.com',
    url='https://github.com/mozilla/tls-canary',
    download_url='https://github.com/mozilla/tls-canary/archive/latest.tar.gz',
    license='MPL2',
    packages=find_packages(exclude=["tests"]),
    include_package_data=False,
    package_data=PACKAGE_DATA,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'dev': DEV_REQUIRES},
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'tlscanary = tlscanary.main:main'
        ]
    }
)
