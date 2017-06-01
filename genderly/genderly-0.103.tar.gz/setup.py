from setuptools import setup
import os
setup(name='genderly',
      version='0.103',
      description='A library to classify an indian name as Male or Female. Mainly focused around making the user onboarding smooth for eCommerce merchants by pre-filling the gender for their users during a signup.',
      url='https://github.com/rajdeltarobo/genderly',
      author='Raj Vardhan Singh',
      author_email='is.rajvardhan@gmail.com',
      license='MIT',
      packages=['genderly'],
      package_data = {
        '': ['*.txt', '*.csv', '*.pkl', '*.npy'],
    },
      data_files=[('genderly/data/', [os.path.join('genderly/data','*.csv'),os.path.join('genderly/data','*.json')]),
                  ('genderly/model', [os.path.join('genderly/model','*.pkl'),os.path.join('genderly/model','*.npy')])],
      zip_safe=False)