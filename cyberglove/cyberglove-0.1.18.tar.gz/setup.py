import numpy as np
from glob import glob
from os.path import join
from setuptools import find_packages, setup, Extension


ext = Extension('cyberglove.cyberglove',
                sources=glob(join('source', '*.c*')),
                extra_compile_args=["-std=c++11"])


setup(name='cyberglove',
      version='0.1.18',
      description='Communicate with cyberglove from python',
      packages=find_packages(),
      author='Alex Ray',
      author_email='a@machinaut.com',
      install_requires=['numpy>=1.12.1', 'pyserial>=3.3'],
      include_package_data=True,
      include_dirs=['source', np.get_include()],
      ext_modules=[ext])
