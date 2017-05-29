#print "hello it's setup py"
from distutils.core import setup
setup(
  name = 'malittlechatapptest1',
  packages = ['malittlechatapptest1'], # this must be the same as the name above
  version = '0.1',
  description = 'this is a chat app for ma self and it is for test only and education purpose ! ',
  author = 'esy H',
  author_email = 'peterldowns@gmail.com',
  url = 'https://github.com/amirhh00', # use the URL to the github repo
  download_url = 'https://github.com/amirhh00/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'chat', 'example'], # arbitrary keywords
  classifiers = [],
)
