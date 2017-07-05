#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

from setuptools import setup

setup(
  name='xPlotUtil',
  version='0.0.4',
  description='The program provides a GUI for the user to graph the data in different forms, normalize and fit it.',
  author='Phaulo C. Escalante',
  author_email='escalante.phaulo@outlook.com',
  url='https://github.com/AdvancedPhotonSource/xPlotUtil',
  packages=['xPlotUtil', ],
  install_requires=['spec2nexus',
                    'pyqt==5.6.0',
                    'matplotlib',
                    'numpy',
                    'future',
                    'pyside==1.2.0',
                    'scipy',
                    'peakutils',
                    ],
  license='See LICENSE File',
  platforms='any',
)
