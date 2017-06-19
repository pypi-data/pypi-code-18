from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='zpython-tools',
      version='0.0.3',
      description='kafka tools with python',
      long_description=readme(),
      keywords='kafka tools built against our env.',
      author='Tony Liu',
      license='MIT',
      packages=find_packages(exclude=["tests", ]),
      install_required=[
          'kazoo.client'
      ],
      scripts=['bin/manage_broker_meta'],
      include_package_date=True,
      zip_safe=False
      )
