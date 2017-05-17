"""
The webappify package
"""
import os
from codecs import open
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.rst'), encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='WebAppify',
    version='0.1',
    description='Create desktop apps of your favourite websites',
    long_description=LONG_DESCRIPTION,
    url='https://launchpad.net/webappify',
    author='Raoul Snyman',
    author_email='raoul@snyman.info',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='Qt website',
    packages=find_packages(),
    install_requires=['PyQt5']
)
