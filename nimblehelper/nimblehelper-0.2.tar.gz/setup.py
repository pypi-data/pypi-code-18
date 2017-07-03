from setuptools import setup

setup(name='nimblehelper',
      version='0.2',
      description='Nimbel Infrastructure Helper',
      author='Brendan Kamp',
      author_email='brendan@tangentsolutions.co.za',
      license='MIT',
      packages=['nimblehelper'],
      install_requires=[
          'djangorestframework',
      ],
      zip_safe=False)
