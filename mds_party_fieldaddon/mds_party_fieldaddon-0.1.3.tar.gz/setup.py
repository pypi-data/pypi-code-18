""" Adds some fields to the 'Party' type
""" 

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import ConfigParser, re

here = path.abspath(path.dirname(__file__))
MODULE = 'party_fieldaddon'
PREFIX = 'mds'

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# tryton.cfg einlesen
config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()

# tryton-version
major_version = 3
minor_version = 8

requires = ['mds-sqlextension >= 0.1.2']
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        prefix = 'trytond'
        requires.append('%s_%s >= %s.%s, < %s.%s' %
                (prefix, dep, major_version, minor_version,
                major_version, minor_version + 1))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

setup(name='%s_%s' % (PREFIX, MODULE),
    version=info.get('version', '0.0.1'),
    description='Tryton module to add some fields to the party-type',
    long_description=long_description,
    url='https://www.m-ds.de/',
    download_url='https://www.m-ds.de/serviceportal/downloads/trytonmodul-party-fieldaddon',
    author='m-ds GmbH',
    author_email='service@m-ds.de',
    license='GPL-3',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Plugins',
    'Framework :: Tryton',
    'Intended Audience :: Developers',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Legal Industry',
    'Topic :: Office/Business',
    'Natural Language :: German',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 2.7',
    ],

    keywords='tryton party',
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        ],
    package_data={
        'trytond.modules.%s' % MODULE: (info.get('xml', [])
            + ['tryton.cfg', 'locale/*.po', 'README.rst','view/*.xml']),
        },

    install_requires=requires,
    zip_safe=False,
    entry_points=""" 
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
)
