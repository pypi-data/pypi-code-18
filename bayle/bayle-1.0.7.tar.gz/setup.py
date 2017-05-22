from distutils.core import setup
setup(
  name = 'bayle',
  packages = ['bayle'],
  version = '1.0.7',
  description = 'A Python package that provides reproducible code and data for my scientific research',
  author = 'Yann Bayle',
  author_email = 'bayle.yann@live.fr',
  url = 'https://github.com/ybayle/research',
  download_url = 'https://github.com/ybayle/research/archive/v1.0.7.tar.gz',
  keywords = ['satin', 'MIR', 'dataset', 'research', 'reproducibility'],
  classifiers = [],
  include_package_data = True,
  license = 'LICENSE.txt',
  install_requires=[
    'requests>=2.9.1',
  ],
  entry_points={
    'console_scripts': [
        'bayle=bayle.satin:main',
    ],
  },
)
