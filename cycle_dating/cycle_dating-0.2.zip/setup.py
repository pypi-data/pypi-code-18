from distutils.core import setup
setup(
  name = 'cycle_dating',
  packages = ['cycle_dating', 'cycle_dating.Algos', 'cycle_dating.Utilities', 'cycle_dating.Algos.Utilities'],
  install_requires = ['numpy', 'pandas', 'matplotlib'],
  version = '0.2',
  description = 'A library for finding cycles in time series. May also be used as a data reduction/filtering method',
  author = 'Konrad Kapp',
  author_email = 'konrad.p.kapp@gmail.com',
  url = 'https://github.com/k-kapp/CycleDating', 
  download_url = 'https://github.com/k-kapp/CycleDating/archive/0.1.tar.gz',
  keywords = ['cycles', 'filtering', 'time series'], 
  classifiers = [],
)