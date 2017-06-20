from setuptools import setup

setup(name='googlespider',
      version='0.1.7',
      description='A command line google spider. Extracts links.',
      # setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
      download_url='https://gitlab.com/hyperion-gray/googlespider/repository/archive.tar.gz?ref=0.1.7',
      url='http://gitlab.com/hyperion-gray/googlespider',
      author='Luke Maxwell',
      author_email='luke@codepunk.xyz',
      license='MIT',
      packages=['googlespider'],
      install_requires=[
          'tldextract',
          'requests',
          'beautifulsoup4',
          'lxml',
          'validators',
      ],
      include_package_data=True,
      package_data={'googlespider': ['config.ini']},
      exclude_package_data={'': ['*.pyc']},
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['googlespider=googlespider.command_line:main'],
      },
      zip_safe=False)
