from setuptools import setup

setup(name='tamme-python',
      version='0.8',
      description='A library for importing and installing tamme analytics from PyPi',
      url='https://bitbucket.org/tamme-io/tamme-python',
      author='tamme',
      author_email='opensource@tamme.io',
      license='MIT',
      packages=[
            'tamme'
      ],
      install_requires=[
            'requests'
      ],
      zip_safe=False)
