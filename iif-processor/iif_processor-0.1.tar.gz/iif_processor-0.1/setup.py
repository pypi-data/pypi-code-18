from setuptools import setup

setup(name='iif_processor',
      version='0.1',
      description='Processes all images in a directory for IIF server',
      url='http://github.com/j0hnds/diva.js',
      author='Dave Sieh',
      author_email='dj0nve@gmail.com',
      license='MIT',
      packages=['iif_processor'],
      scripts=['bin/iif_process.py'],
      zip_safe=False)
