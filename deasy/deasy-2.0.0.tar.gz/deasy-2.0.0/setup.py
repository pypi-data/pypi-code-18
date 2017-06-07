from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '2.0.0'

setup(
    name='deasy',
    version=version,
    description="Simple CLI to manage Odoo instances",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='odoo backup restore security',
    author='Mohamed Cherkaoui',
    author_email='chermed@gmail.com',
    url='https://github.com/chermed/deasy',
    license='LGPL v3',
    py_modules=['deasy'],
    include_package_data=True,
    install_requires=[
        'click',
        'odoorpc',
        'prettytable',
        'ConfigParser',
        'XlsxWriter',
    ],
    entry_points='''
        [console_scripts]
        oo=oo:main
    ''',
)