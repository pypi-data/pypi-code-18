from setuptools import setup, find_packages

setup(name='pyHelfrag',
      version='0.2b',
      description='Generate (U-Th)/He Apatite fragment ages',
      url='',
      author='Romain Beucher',
      author_email='romain.beucher@unimelb.edu.au',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='apatite, diffusion, helfrag, U-Th/He',
      packages=['pyHelfrag'],
      install_requires=['scipy', 'numpy', 'pandas', 'matplotlib', 'tqdm'])
