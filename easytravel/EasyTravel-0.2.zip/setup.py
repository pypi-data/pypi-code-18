from distutils.core import setup
setup(
  name = 'EasyTravel',
  packages = ['EasyTravel'],
  version = '0.2',
  description = 'Module for searching flight tickets based on Skyscanner API',
  author = 'Bohdan Borkivskyy',
  author_email = 'b.borkivskyy@ucu.edu.ua',
  url = 'https://github.com/BohdanBorkivskyy/EasyTravel',
  download_url = 'https://github.com/BohdanBorkivskyy/EasyTravel/archive/0.2.tar.gz',
  keywords = ['travel', 'skyscanner', 'flight'],
  classifiers = [],
  install_requires=['pygame==1.9.3']
)