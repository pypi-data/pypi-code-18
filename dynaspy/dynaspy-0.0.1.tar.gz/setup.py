from distutils.core import setup
setup(
  name = 'dynaspy',
  packages = ['dynaspy'],
  version = '0.0.1',
  description = 'A simple python wrapper for the Dynasty API',
  author = 'Dynasty Research',
  author_email = 'dan@dynasty.com',
  url = 'https://github.com/dynasty-com/dynaspy.git', 
  keywords = ['dynasty'],
  classifiers = ['Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'],
  license = 'MIT',
  install_requires=['pandas']
)