from setuptools import setup, find_packages

from snek import __title__, __version__, __author__, __description__, \
    __license__, __url__

setup(
    name=__title__,
    version=__version__,
    packages=find_packages(),
    url=__url__,
    license=__license__,
    author=__author__,
    author_email='',
    description=__description__,
    entry_points={
        'console_scripts': ['dotsnek = snek.main:main']
    }
)
