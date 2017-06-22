from setuptools import setup

setup(name='yolapiAsync',
      version='0.1.1',
      description='A basic async wrapper around the Rainbird API',
      url='http://rainbird.ai',
      author='craigbot',
      author_email='craig.cochran@rainbird.ai',
      license='MIT',
      packages=['yolapiAsync'],
      classifiers=[
            "Development Status :: 3 - Alpha"
      ],
      install_requires=[
            'aiohttp'
      ])