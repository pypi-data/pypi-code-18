from distutils.core import setup

setup(
name = 'speake3',
packages = ['speake3'], # this must be the same as the name above
version = '0.1',
description = 'A wrapper for espeak for python3',
long_description=open('README.md').read(),
license='MIT',
platforms='Linux',
author = 'Brian Gikonyo',
author_email = 'colasgikonyo@gmail.com',
url = 'https://github.com/GikonyoBrian/speake3', # use the URL to the github
download_url = 'https://github.com/GikonyoBrian/speake3/archive/speake3.tar.gz',
keywords = ['espeak', 'tts', 'text-to-speech', 'engine', 'python3', 'python'], 
classifiers = [
	'Development Status :: 3 - Alpha',
 	'Environment :: Console',
 	'Intended Audience :: Developers',
 	'Programming Language :: Python',
 	'Programming Language :: Python :: 3',
 	'Programming Language :: Python :: 3.0',
 	'Programming Language :: Python :: 3.1',
 	'Programming Language :: Python :: 3.2',
 	'Programming Language :: Python :: 3.3',
 	'Programming Language :: Python :: 3.4'],
)