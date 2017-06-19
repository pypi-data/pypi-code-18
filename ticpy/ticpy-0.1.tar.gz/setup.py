import os

from setuptools import setup

requires = ['bunch==1.0.1']

setup(name='ticpy',
      version='0.1',
      description='ticpy',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Rahul Gupta',
      author_email='rahul1990gupta@gmail.com',
      url='https://github.com/rahul1990gupta/TicPy',
      keywords='tic tac toe in python',
      packages=['ticpy'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points=dict(
          console_scripts=[
              'ticpy = ticpy.game:main',
          ]
      )
)