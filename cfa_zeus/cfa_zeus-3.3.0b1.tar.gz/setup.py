from setuptools import setup
import glob
import os

exec(compile(open('zeus/_version.py').read(), 'zeus/_version.py', 'exec'))

setup(name='cfa_zeus',
      version = __version__,
      description = 'general tools: cryptography, file, parsing, log',
      url = 'https://github.com/cfauchard/zeus',
      author = 'Christophe Fauchard',
      author_email = 'christophe.fauchard@gmail.com',
      license = 'GPLV3',
      packages = ['zeus'],
      scripts = ['bin/zkey.py', 'bin/zcrypt.py'],
      data_files = [
            (
                  'sample/zeus', [
                        f for f in glob.glob(
                              os.path.join('sample', '*.py')
                        )
                  ] + [
                        f for f in glob.glob(
                              os.path.join('sample', '*.ini')
                        )
                  ] + [
                        f for f in glob.glob(
                              os.path.join('sample', '*.xml')
                        )
                  ]
            )
      ],
      zip_safe = False)
