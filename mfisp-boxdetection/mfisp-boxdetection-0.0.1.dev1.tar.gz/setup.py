# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages


import numpy
try:
    from Cython.Build import cythonize
    use_cython = True
except ImportError:
    use_cython = False

setup(
    name='mfisp-boxdetection',
    version='0.0.1.dev1',
    description='mfisp-boxdetection',
    long_description='mfisp-boxdetection, see https://github.com/csachs/mfisp-boxdetection for info',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='https://github.com/csachs/mfisp-boxdetection',
    packages=find_packages(),
    ext_modules=cythonize('mfisp_boxdetection/fast_argrelextrema.pyx') if use_cython else None,
    include_dirs=[numpy.get_include()],
    package_data={
        'mfisp_boxdetection': ['fast_argrelextrema.pyx']
    },
    install_requires=['numpy', 'molyso'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ]
)
