import setuptools

setuptools.setup(name='pyfea',
      version='1.0.0.dev1',
      description='Python Finite Element Analysis',
      url='https://github.com/schang1146/pyfea',
      author='team.pyfea',
      author_email='team.pyfea@gmail.com',
      license='MIT',
      classifiers=[
      # Maturity of project:
      #     3 - Alpha
      #     4 - Beta
      #     5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Specify license (should match "license" above)
      'License :: OSI Approved :: MIT License',

      # Indicate audience
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering',

      # Specify supported Python versions
      'Programming Language :: Python :: 3',
      ],
      keywords='engineering development analysis',
      packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
      zip_safe=False)
