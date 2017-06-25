# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 15:27:01 2017

@author: Caiyd
"""

from setuptools import setup, find_packages


VERSION = '0.1.0'


setup(name='cnvcallertools',
      version=VERSION,
      description='command line tool kits from analysis CNVcaller result',
      keywords='python cnvcaller commandline',
      author='YudongCai',
      author_email='yudongcai216@gmail.com',
      license='MIT',
      url='https://github.com/silvewheat/CNVcaller_tools',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
              'click',
              'numpy',
              'scipy',
              'pandas'
              ],
      entry_points={
              'console_scripts': [
                      'cnvtk = cnvcallertools.main:main'
                      ]
              }
      )