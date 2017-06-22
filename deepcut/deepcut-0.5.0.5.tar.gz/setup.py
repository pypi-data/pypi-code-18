"""
Thai word Segmentation using Convolutional Neural Network
"""

from distutils.core import setup
import setuptools

setup(
  name = 'deepcut',
  packages = ['deepcut'], 
  package_dir={'deepcut': 'deepcut'},
  package_data={'deepcut': ['weight/*']},
  version = '0.5.0.5',
  install_requires=['keras', 'pandas', 'scipy', 'numpy'],
  license='MIT',
  description = 'A Thai word tokenization library using Deep Neural Network',
  author = 'Rakpong Kittinaradorn',
  author_email = 'r.kittinaradorn@gmail.com',
  url = 'https://github.com/rkcosmos/deepcut',
  download_url = 'https://github.com/rkcosmos/deepcut/package/0.5.zip', 
  keywords = ['thai word segmentation deep learning neural network development'],
  classifiers = ['Development Status :: 3 - Alpha'],
  #data_files=[('deepcut', ['deepcut/utils.py']),
  #('deepcut/weight', ['deepcut/weight/best_cnn.h5']),
  #('deepcut/weight', ['deepcut/weight/object.pk']),
  #],
)
