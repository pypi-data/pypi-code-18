import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name = 'integra-setup',
  packages=find_packages(),
  include_package_data=True,
  version = '0.1',
  description = 'A django setup app with angularjs and bootstrap',
  author = 'Partha.Konda',
  author_email = 'parthasaradhi1992@gmail.com',
  url = '', 
  download_url = '', 
  keywords = ['django-setup', 'integra-setup'], 
  classifiers = [],
  install_requires=[
        "django",
        "integra-authentication"
    ],
  zip_safe=True)
