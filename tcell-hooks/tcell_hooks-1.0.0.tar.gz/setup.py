from setuptools import setup, find_packages
from tcell_hooks.version import VERSION

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    name='tcell_hooks',
    version=VERSION,
    description='Allows custom event sending of login failures/success to TCell',
    url='https://tcell.io',
    author='tCell.io',
    author_email='support@tcell.io',

    license='No License',
    install_requires=[],
    tests_require=[],
    packages=find_packages()
)
