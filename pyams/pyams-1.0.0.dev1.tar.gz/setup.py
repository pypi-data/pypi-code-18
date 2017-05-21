import setuptools

setuptools.setup(name='pyams',
      version='1.0.0.dev1',
      description='Python Aerospace Mechanics & Structures',
      url='https://github.com/schang1146/pyams',
      author='team.pyams',
      author_email='team.pyams@gmail.com',
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
      keywords='aerospace engineering development',
      packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
      zip_safe=False)
