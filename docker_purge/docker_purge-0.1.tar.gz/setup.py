from setuptools import setup

setup(name='docker_purge',
      version='0.1',
      description='One command to rule all purges on your docker engine.',
      url='https://github.com/matglas/docker_purge.git',
      author='Matthias Glastra',
      author_email='matthias@vdmi.nl',
      license='MIT',
      packages=['docker_purge'],
      scripts=['bin/docker-purge'],
      entry_points={
          'console_scripts': ['docker-purge=docker_purge:purge_commandline'],
      },
      zip_safe=False, install_requires=['docker'])
