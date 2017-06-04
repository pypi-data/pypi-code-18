#!/usr/bin/env python

from distutils.core import setup

setup(name='WebViewHandler',
      version='0.2',
      description='Logging handler that provides scrolling web view',
      author='John Fink',
      author_email='johnfink8@gmail.com',
      packages=['WebViewHandler', ],
      package_data={'WebViewHandler': ['templates/base.html']},
      url='https://github.com/johnfink8/WebViewHandler',
      download_url = 'https://github.com/johnfink8/WebViewHandler/archive/0.2.tar.gz'
      )
