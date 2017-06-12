from distutils.core import setup
setup(
  name = 'socratatodatadotworld',
  packages = ['socratatodatadotworld'], # this must be the same as the name above
  version = '0.1.2',
  description = 'Copies Socrata datasets to data.world',
  author = 'Tim Clemans',
  author_email = 'tim@hardworkingcoder.com',
  url = '', # use the URL to the github repo
  download_url = 'https://github.com/hardworkingcoder/socrata-to-datadotworld/archive/0.1.2.tar.gz',
  keywords = ['data copying'], # arbitrary keywords
  classifiers = [],
  scripts=['bin/socrata-to-datadotworld'],
  install_requires=[
      'requests',
      'datadotworld',
      'click'
  ],
)
