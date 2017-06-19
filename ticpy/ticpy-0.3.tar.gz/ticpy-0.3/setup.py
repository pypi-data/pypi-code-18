import os

from setuptools import setup

requires = ['bunch==1.0.1',
            'pytest-cov==2.5.1',
            'pytest-mock==1.6.0',
            'codecov==2.0.9',
            'pytest==3.1.2'
            ]

setup(name='ticpy',
      version='0.3',
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
              'ticpy = ticpy.src.game:main',
          ]
      )
)