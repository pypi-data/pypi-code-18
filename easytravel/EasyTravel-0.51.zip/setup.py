from distutils.core import setup
setup(
  name = 'EasyTravel',
  packages = ['easytravel'],
  version = '0.51',
  description = 'Module for searching flight tickets based on Skyscanner API',
  author = 'Bohdan Borkivskyy',
  author_email = 'b.borkivskyy@ucu.edu.ua',
  url = 'https://github.com/BohdanBorkivskyy/EasyTravel',
  download_url = 'https://github.com/BohdanBorkivskyy/EasyTravel/archive/0.51.tar.gz',
  keywords = ['travel', 'skyscanner', 'flight'],
  classifiers = [],
  install_requires=['pygame==1.9.3', 'skyscanner==1.1.4']
)