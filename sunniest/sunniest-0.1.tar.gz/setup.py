from setuptools import setup

setup(name='sunniest',
      version='0.1',
      description='The Sunniest day in the world',
      url='https://github.com/pypa//sunniest',
      author='Tejashree Jagtap',
      author_email='tjagtap@apple.com',
      license='Apple',
      packages=['sunniest'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)
