from setuptools import setup

setup(name='mrlpy',
      version='0.2',
      description='Python API to MyRobotLab',
      url='http://github.com/autonomicperfectionist/mrlpy',
      author='AutonomicPerfectionist',
      author_email='bwtbutler@hotmail.com',
      license='GPL',
      packages=['mrlpy', 'org.myrobotlab.service'],
      install_requires=['requests', 'websocket-client', 'json'],
      zip_safe=False)
