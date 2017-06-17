from setuptools import setup, Extension

module1 = Extension('ketcham',
                    include_dirs=['./include'],
                    sources = ['./src/Ketcham.c'])

setup(name='pyAFT',
      version='0.1b',
      description='Apatite Fission Track utilities',
      url='',
      author='Romain Beucher',
      author_email='romain.beucher@unimelb.edu.au',
      license='MIT',
      packages=['pyAFT','pyAFT.thermal_histories'],
      keywords='apatite, fission-track, thermochronology',
      install_requires=['numpy','matplotlib','scipy'],
      ext_modules=[module1],
      classifiers= ['Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6']
      )

