from setuptools import setup, find_packages, Extension
import os
try:
    from Cython.Build import cythonize
except:
    print('Cython is required to install PySAIS')
    raise
try:
    import numpy as np
except:
    print('numpy is required to install PySAIS')
    raise

# Pick up a flag for the GLIBC fix.
glibc_fix = (False if 'GLIBC_FIX' not in os.environ else
             os.environ['GLIBC_FIX'] in
             {'Y', 'YES', 'y', 'yes', 'Yes', 'True', 'true', '1'})

compile_args = ['-O3', '-fomit-frame-pointer']
if glibc_fix:
    compile_args.append('-DGLIBC_FIX')

extensions = [Extension('PySAIS._sais32',
                        sources=['PySAIS/_sais32.pyx', 'PySAIS/sais32.c'],
                        extra_compile_args=compile_args),
              Extension('PySAIS._sais64',
                        sources=['PySAIS/_sais64.pyx', 'PySAIS/sais64.c'],
                        extra_compile_args=compile_args)]


setup(
    name='PySAIS',
    version='1.0.4',
    ext_modules=cythonize(extensions, include_path=[np.get_include()]),
    include_dirs=[np.get_include()],
    packages=find_packages(),
    install_requires=['Cython', 'numpy'],
    description='Suffix array computation with induced sorting algorithm.',
    long_description='PySAIS is a wrapper to Yuta Mori\'s implementation of '
                     'the induced sorting algorithm to create suffix arrays. '
                     'Both 32 bit and 64 bit indices are supported and '
                     'automatically recognised.\n\n'
                     'If you encounter a GLIBC_2.14 not found error, try '
                     're-installing with the environment variable GLIBC_FIX=1 '
                     'set.\n\n'
                     'Please raise issues on the tracker on bitbucket: '
                     'https://bitbucket.org/alex-warwickvesztrocy/pysais',
    license='MIT',  # Wrapped library is under MIT license.
    url='https://bitbucket.org/alex-warwickvesztrocy/pysais'
)
