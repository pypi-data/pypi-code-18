from setuptools import setup

setup(name='snapbuy',
      version='1.0',
      description='Snapbuy Python SDK',
      author='Minh Hoang TO',
      author_email='hoang281283@gmail.com',
      packages=['snapbuy'],
      install_requires=[
          'requests==2.13.0',
      ],
      zip_safe=False)
