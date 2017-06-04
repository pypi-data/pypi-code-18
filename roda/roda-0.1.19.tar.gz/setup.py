from setuptools import setup, find_packages

from src import __version__

setup(
    name='roda',
    version=__version__,
    packages=['src'],
    package_dir={'roda': 'src'},
    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
