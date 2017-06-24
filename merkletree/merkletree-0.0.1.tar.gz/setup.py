from setuptools import setup
from merkletree import __version__
__version__ = list(map(str, __version__))


setup(name='merkletree',
      version='.'.join(__version__),
      description='Simple Merkle Tree datastructure',
      url='http://github.com/theSage21/merkletree',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      license='MIT',
      packages=['merkletree'],
      include_package_data=True,
      install_requires=['pycrypto'],
      keywords=['merkle', 'tree'],
      zip_safe=False)
