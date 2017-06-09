from setuptools import setup
from rlagents import __version__
__version__ = list(map(str, __version__))

setup(name='rlagents',
      version='.'.join(__version__),
      description='Reinforcement Learning Agents',
      url='http://github.com/theSage21/rlagents',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      license='MIT',
      packages=['rlagents'],
      install_requires=['tqdm', 'ujson', 'gym'],
      keywords=['rlagents', 'reinforcement', 'learning'],
      zip_safe=False)
