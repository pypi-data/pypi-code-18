from setuptools import setup
import sys
import os
from setuptools.command.install import install


class Custom(install):
    def run(self):
        os.system(
            'wget https://www.cs.toronto.edu/~frossard/vgg16/vgg16_weights.npz')
        install.run(self)


setup(name='dvd',
      description='Deep Vision library for Dummies',
      version='0.1.0',
      author='Ajay Prasadh V, Arnav Varma',
      author_email='ajayrfhp1710@gmail.com',
      packages=['dvd'],
      entry_points={
          'console_scripts': ['dvd=dvd:main'],
      },
      cmdclass={
          'install': Custom
      },
      scripts=[
          'get_vgg.py'
      ],
      url='https://github.com/ajayrfhp/dvd',
      keywords=['Deep learning', 'Computer Vision',
                'Vision', 'Machine learning'],
      classifiers=[
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities'
      ],
      )
