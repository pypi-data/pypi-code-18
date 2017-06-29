from setuptools import setup

setup(name='micropython-bootstrap',
      version='0.1',
      description='Simplified way to build and deploy apps to IoT devices that use micropython',
      url='http://github.com/jbilligmeier/micropython-bootstrap',
      author='Josh Billigmeier',
      author_email='joshua@billigmeier.org',
      license='MIT',
      packages=['micropython'],
      zip_safe=True,
      entry_points = {
        'console_scripts':
        ['bootstrap=micropython.bootstrap:main'],
                      }
      )
