from distutils.core import setup

setup(name='fh',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Feed handler: Incorporate feeds as MH folders',
      url='https://thomaslevine.com/scm/fh/',
      packages=['fh'],
      install_requires=[
          'feedparser>=5.2.1',
          'requests>=2.11.0',
      ],
      tests_require=[
          'pytest>=2.6.4',
      ],
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      entry_points = {'console_scripts': ['fh = fh:main']},
      version='0.0.2',
      license='AGPL',
      )
