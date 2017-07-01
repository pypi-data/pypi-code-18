# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages


try:
    import numpy
    from Cython.Build import cythonize
    use_cython = True
except ImportError:
    print("Either numpy or cython is unavailable, skipping (optional) speed-up functions ...")
    use_cython = False

setup(
    name='mfisp-boxdetection',
    version='0.0.1.dev2',
    description='mfisp-boxdetection',
    long_description='mfisp-boxdetection, see https://github.com/csachs/mfisp-boxdetection for info',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='https://github.com/csachs/mfisp-boxdetection',
    packages=find_packages(),
    ext_modules=cythonize('mfisp_boxdetection/fast_argrelextrema.pyx') if use_cython else None,
    include_dirs=[numpy.get_include()] if use_cython else [],
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
