from distutils.core import setup
setup(
  name = 'mydacoclient',
  packages = ['mydacoclient'],
  install_requires=[
    'requests',
  ],
  version = '1.1.1',
  description = 'python client for mydaco',
  author = 'Benjamin Bach',
  author_email = 'benjamin.bach@mydaco.com',
  url = 'https://github.com/mydaco/python-client',
  download_url = 'https://github.com/mydaco/python-client/archive/master.zip',
  keywords = ['mydaco', 'client'],
  classifiers = [],
)
