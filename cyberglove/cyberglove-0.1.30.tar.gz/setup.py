from glob import glob
from os.path import join
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    # From https://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py

    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


ext = Extension('cyberglove.cyberglove',
                sources=glob(join('source', '*.c*')),
                extra_compile_args=["-std=c++11"])


setup(name='cyberglove',
      version='0.1.30',
      description='Communicate with cyberglove from python',
      packages=find_packages(),
      author='Alex Ray',
      author_email='a@machinaut.com',
      install_requires=['numpy>=1.12.1', 'pyserial>=3.3'],
      cmdclass={'build_ext': build_ext},
      setup_requires=['numpy'],
      include_package_data=True,
      include_dirs=['source'],
      ext_modules=[ext])
