from pip.req import parse_requirements
import setuptools


# Filters out relative/local requirements (i.e. ../lib/utils)
remote_requirements = '\n'.join(str(r.req) for r in parse_requirements("requirements.txt", session='dummy') if r.req)

setuptools.setup(
  name='remoteconfig',
  version='1.0.0',

  author='Max Zheng',
  author_email='maxzheng.os @t gmail.com',

  description='A simple wrapper for localconfig that allows for reading config from a remote server',
  long_description=open('README.rst').read(),

  url='https://github.com/maxzheng/remoteconfig',

  install_requires=remote_requirements,

  license='MIT',

  packages=setuptools.find_packages(),
  include_package_data=True,

  setup_requires=['setuptools-git'],

  classifiers=[
    'Development Status :: 5 - Production/Stable',

    'Intended Audience :: Developers',
    'Topic :: Software Development',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
  ],

  keywords='configuration remote http config',
)
