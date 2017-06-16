from setuptools import setup
setup(
  name = 'py2sh',
  packages = ['py2sh'], # this must be the same as the name above
  version = '0.0.1',
  license='MIT',
  description = 'A python CLI for busy scientists',
  author = 'Akiva Lipshitz',
  author_email = 'aclscientist@gmail.com',
  entry_points={
      'console_scripts':[
          "py2sh=py2sh:py2sh_demo"
       ]
  },
  url = 'https://github.com/theideasmith/py2sh', # use the URL to the github repo
  download_url = 'https://github.com/theideasmith/py2sh/archive/0.0.1.tar.gz', # I'll explain this in a second
  keywords = ['cli', 'command', 'argparse', 'click', 'script', 'function','bash', 'py2sh'], # arbitrary keywords
  classifiers = [],
)
