from setuptools import setup

VERSION = '0.1.0'
REPO = 'https://github.com/bitlang/kabob'

setup(
    name='kabob',
    packages=['kabob'],
    version=VERSION,
    description='Skewer your objects with complex iterators',
    author='Josh Junon',
    author_email='josh@junon.me',
    url=REPO,
    download_url='{}/archive/{}.tar.gz'.format(REPO, VERSION),
    keywords=['_', 'iterator', 'object', 'compose'],
    classifiers=[],
    install_requires=[],
    dependency_links=[]
)
