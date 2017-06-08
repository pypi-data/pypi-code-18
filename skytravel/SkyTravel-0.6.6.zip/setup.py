from distutils.core import setup
setup(
  name = 'SkyTravel',
  packages = ['skytravel'],
  version = '0.6.6',
  description = 'Module for searching flight tickets based on Skyscanner API',
  author = 'Bohdan Borkivskyy',
  author_email = 'b.borkivskyy@ucu.edu.ua',
  url = 'https://github.com/BohdanBorkivskyy/SkyTravel',
  download_url = 'https://github.com/BohdanBorkivskyy/SkyTravel/archive/0.6.6.tar.gz',
  keywords = ['travel', 'skyscanner', 'flight'],
  classifiers = [],
  install_requires=['pygame==1.9.3', 'skyscanner==1.1.4']
)