from setuptools import setup

setup(name='nimblehelper',
      version='0.1',
      description='Nimbel Infrastructure Helper',
      author='Brendan Kamp',
      author_email='brendan@tangentsolutions.co.za',
      license='MIT',
      packages=['nimblehelper'],
      install_requires=[
          'rest_framework',
      ],
      zip_safe=False)
