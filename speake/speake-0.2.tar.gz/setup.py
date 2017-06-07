from distutils.core import setup

setup(
name = 'speake',
packages = ['speake'], # this must be the same as the name above
version = '0.2',
description = 'A wrapper for espeak for python2',
license='MIT',
platforms='Linux',
author = 'Brian Gikonyo',
author_email = 'colasgikonyo@gmail.com',
url = 'https://github.com/GikonyoBrian/speake', 
download_url = 'https://github.com/GikonyoBrian/speake/archive/speake.tar.gz',
keywords = ['espeak', 'tts', 'text-to-speech', 'engine', 'python2', 'python'],
classifiers = [
	'Development Status :: 3 - Alpha',
 	'Environment :: Console',
 	'Intended Audience :: Developers',
 	'Programming Language :: Python',
 	'Programming Language :: Python :: 2',
 	'Programming Language :: Python :: 2.6',
 	'Programming Language :: Python :: 2.7',],
)