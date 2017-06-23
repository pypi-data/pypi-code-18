"""
Thai word Segmentation using Convolutional Neural Network
"""

#from distutils.core import setup
from setuptools import setup

setup(
  name = 'deepcut',
  packages = ['deepcut'], 
  package_dir={'deepcut': 'deepcut'},
  package_data={'deepcut': ['weight/*']},
  include_package_data=True,
  version = '0.5.0.14',
  install_requires=['keras', 'pandas', 'scipy', 'numpy'],
  license='MIT',
  description = 'A Thai word tokenization library using Deep Neural Network',
  author = 'Rakpong Kittinaradorn',
  author_email = 'r.kittinaradorn@gmail.com',
  url = 'https://github.com/rkcosmos/deepcut',
  download_url = 'https://github.com/rkcosmos/deepcut/package/0.5.zip', 
  keywords = ['thai word segmentation deep learning neural network development'],
  classifiers = ['Development Status :: 3 - Alpha'],
)
