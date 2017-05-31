from distutils.core import setup
import os

# Please run
# python setup.py install   

setup(
	name = 'gmailfs-fuse',
	version = '0.8.6',
	author = 'Mahdi Mokhtari',
	url = 'https://github.com/mmokhi/gmailfs',
	packages = ['gmailfs-fuse'],
	package_dir = {'gmailfs-fuse':'src/gmailfs/'},
	scripts = ['src/gmailfs/mount_gmailfs'],
	data_files = [('/usr/local/etc/gmailfs/', ['src/gmailfs/conf/gmailfs.conf'])],
)
