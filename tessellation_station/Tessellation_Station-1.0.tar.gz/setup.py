from setuptools import setup

setup(
      name='Tessellation_Station',
      version='1.0',
      description='Basic polygon tessellation on the command line',
      url='https://github.com/edison-moreland/Tessellation-Station',
      download_url='https://github.com/edison-moreland/Tessellation-Station/archive/1.0.0.tar.gz',
      author='Edison Moreland',
      author_email='edison@devdude.net',
      license='MIT',
      packages=[
            'tessellation_station',
      ],
      entry_points={
            'console_scripts': [
                  'tessellation_station = tessellation_station.main:from_file'
            ]
      },
      install_requires=[
            'Pillow',
      ],
      setup_requires=[
            'pytest-runner',
      ],
      tests_require=[
            'pytest',
      ],
      )