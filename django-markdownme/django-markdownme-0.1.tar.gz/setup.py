#from distutils.core import setup
#setup(
  #name = 'django-markdownme',
  #packages = ['django-markdownme'], # this must be the same as the name above
  #version = '0.1',
  #description = 'Text editor component with Markdown syntax support, file upload manager and history of changes.',
  #author = 'Oliver Kovac',
  #author_email = 'oliver.kovac.2@student.tuke.sk',
  #url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  #download_url = 'https://github.com/peterldowns/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
  #keywords = ['Django', 'Markdown', 'file upload', 'history', 'preview',], # arbitrary keywords
  #classifiers = [],
#)

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-markdownme',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A Django text editor with Markdown and file upload support',
    long_description=README,
    url='https://github.com/oliverkovac/django-markdownme',
    author = 'Oliver Kovac',
    author_email = 'oliver.kovac.2@student.tuke.sk',
    install_requires=[
        'markdown',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)