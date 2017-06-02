from distutils.core import setup

setup(
  name = 'phantomrestclient',
  packages = ['phantomrestclient'], # this must be the same as the name above
  version = '0.1.1',
  description = 'A wrapper library around the Phantom Rest API.',
  author = 'Joe Ingalls',
  author_email = 'joe.ingalls@optiv.com',
  url = 'https://bitbucket.org/jingalls/phantomrestclient', # use the URL to the github repo
  # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['phantom', 'phantomcyber'], # arbitrary keywords
  classifiers = [
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
  ],
)
