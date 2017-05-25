from distutils.core import setup

setup(name='speed-test',
      version='0.1',
      description='Application to report bandwidth of network',
      url='https://github.com/Rohithyeravothula/speed-test',
      author='Rohith Y',
      author_email='rohithiitj@gmail.com',
      license='MIT',
      packages=['speedApp'],
      install_requires=[
          'speedtest-cli==1.0.6',
			'wheel==0.24.0'
      ],
      zip_safe=False)
