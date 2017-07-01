import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name = 'integra-chore',
  packages=find_packages(),
  include_package_data=True,
  version = '1.0.6',
  description = 'A django chore app with angularjs and bootstrap',
  author = 'Partha.Konda',
  author_email = 'parthasaradhi1992@gmail.com',
  url = '', 
  download_url = '', 
  keywords = ['django-authentication', 'integra-authentication'], 
  classifiers = [],
  install_requires=[
        "django",
        "integra-authentication",
        "integra-setup",
        "djangorestframework"
    ],
  zip_safe=True)
