"""
DirbleWrapper
--------------
DirbleWrapper is a small program to wrap the dirble api
"""

from setuptools import setup, find_packages
import os


BASE_PATH = os.path.dirname(__file__)


setup(
    name='Dirble-Wrapper',
    version="0.1.0",
    url='https://github.com/speedy1991/DirbleWrapper',
    license='MIT',
    author='Arthur Holzner',
    author_email='arthur.holz.91@gmail.com',
    description='DirbleWrapper is a small program to wrap the dirble api',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
#   install_requires=None,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)