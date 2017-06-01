from distutils.core import setup
setup(
  name = 'SkyTravel',
  packages = ['SkyTravel'],
  version = '0.6.1',
  description = 'Module for searching flight tickets based on Skyscanner API',
  author = 'Bohdan Borkivskyy',
  author_email = 'b.borkivskyy@ucu.edu.ua',
  url = 'https://github.com/BohdanBorkivskyy/SkyTravel',
  download_url = 'https://github.com/BohdanBorkivskyy/SkyTravel/archive/0.6.1.tar.gz',
  keywords = ['travel', 'skyscanner', 'flight'],
  classifiers = [],
  install_requires=['pygame==1.9.3', 'skyscanner==1.1.4']
)