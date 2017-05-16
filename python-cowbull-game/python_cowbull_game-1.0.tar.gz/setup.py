from setuptools import setup

setup(name='python_cowbull_game',
      version='1.0',
      description='Python cowbull game object',
      url='https://github.com/dsandersAzure/python_cowbull_game',
      author='David Sanders',
      author_email='dsanderscanadanospam@gmail.com',
      license='Apache License 2.0',
      packages=['python_cowbull_game'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'python-digits',
          'jsonschema',
      ],
      zip_safe=False)
