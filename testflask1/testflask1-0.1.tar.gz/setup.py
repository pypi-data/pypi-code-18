from setuptools import setup

setup(name='testflask1',
      version='0.1',
      description='testflask1 dependency',
      url='https://github.com/pypa/testflask1',
      author='Tejashree Jaagtap',
      author_email='tjagtap@apple.com',
      license='Apple',
      packages=['main'],
      install_requires=[
             'Flask'
      ],
      dependency_links=['https://github.com/pallets/flask/archive/master.tar.gz'],
      zip_safe=False)