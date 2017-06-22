from setuptools import setup

setup(name='pysharefile',
      version='0.1',
      description='Utility modules for working with Sharefile in python 3',
      url='http://github.com/storborg/funniest',
      author='Austin Nafziger',
      author_email='anafziger@42northrx.com',
      license='MIT',
      packages=['pysharefile'],
      install_requires=[
          'json',
          'http',
          'mimetypes',
          'time',
          'urllib',
      ],
      zip_safe=False)