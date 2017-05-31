#-*- coding:utf-8 -*-

from distutils.core import setup
from setuptools import find_packages


setup(name='index_analysis',
    version='1.0.0',
    author = 'cc',
    author_email='criller@163.com',
    maintainer='criller',
    maintainer_email='criller@163.com',
    url = 'https://www.baidu.com',
    description='this is cc test setup case',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    license='BSD License',
    platforms=['all'],
    install_requires = ["sqlalchemy"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
   ]
)
