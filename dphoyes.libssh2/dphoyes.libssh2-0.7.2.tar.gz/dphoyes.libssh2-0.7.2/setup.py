import sys
from distutils.core import setup, Extension

VERSION = '0.7.2'

setup(
  name='dphoyes.libssh2',
  version=VERSION,
  ext_modules=[Extension('libssh2',
    sources=[
      'src/ssh2.c',
      'src/session.c',
      'src/channel.c',
      'src/sftp.c',
      'src/sftphandle.c',
      'src/listener.c'
    ],
    depends=[
      'src/ssh2.h',
      'src/session.h',
      'src/channel.h',
      'src/sftp.h',
      'src/sftphandle.h',
      'src/listener.h'
    ],
    libraries=['ssl', 'crypto', 'ssh2', 'z'],
    define_macros=[('MODULE_VERSION', '"%s"' % VERSION)]
  )],
  description='Python bindings for libssh2',
  author='Sebastian Noack',
  author_email='sebastian.noack@gmail.com',
  url='https://github.com/dphoyes/ssh4py',
  download_url='https://github.com/dphoyes/ssh4py/archive/%s.tar.gz' % VERSION,
  license='LGPL',
)
