from setuptools import setup

setup(name='rpihware',
      version='0.1',
      description='A layer to control common elements in raspberry pi 3 via GPIO',
      url='',
      author='kneerunjun',
      author_email='kneerunjun@gmail.com',
      license='MIT',
      packages=['rpihware'],
      install_requires=[
          'rpi.gpio','Adafruit_CharLCD'
      ],
      zip_safe=False)
