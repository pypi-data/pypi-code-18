from distutils.core import setup
setup(
  name = 'borkivskyy_coursework',
  packages = ['borkivskyy_coursework'], # this must be the same as the name above
  version = '0.3',
  description = 'Anton Borkivskyy\'s coursework',
  author = 'Anton Borkivskyy',
  author_email = 'borkivskyy@ucu.edu.ua',
  url = 'https://github.com/AntonBorkivskyy/coursework', # use the URL to the github repo
  download_url = 'https://github.com/peterldowns/mypackage/archive/0.3.tar.gz', # I'll explain this in a second
  keywords = ['coursework'], # arbitrary keywords
  classifiers = [],
  install_requires=['itunespy==1.5.3']
)