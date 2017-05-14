try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from dasha import __version__, __author__

setup(
    name='dasha',
    version=__version__,
    author=__author__,
    author_email='serbernar1@gmail.com',
    url='https://github.com/serbernar/dasha',
    description='find word or words in text',
    download_url='https://github.com/serbernar/dasha/archive/master.zip',
    license='MIT',
    packages=['dasha'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
