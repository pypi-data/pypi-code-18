from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.2.0'

setup(
    name='dyz',
    version=version,
    description="Simple CLI to manage Odoo instances",
    long_description=README,
    classifiers=[
    ],
    keywords='odoo backup restore security',
    author='Mohamed Cherkaoui',
    author_email='chermed@gmail.com',
    url='https://github.com/chermed/dyz',
    license='LGPL v3',
    py_modules=['dyz'],
    include_package_data=True,
    install_requires=[
        'click',
        'odoorpc',
        'prettytable',
        'ConfigParser',
        'XlsxWriter',
        'lxml',
    ],
    entry_points='''
        [console_scripts]
        dyz=dyz:main
    ''',
)
