from setuptools import setup

setup(name='pyspotless',
      version='0.9.4',
      description='A client library for integrating spotlessdata.com into Python applications',
      url='https://bitbucket.org/tom-weiss/pyspotless',
      author='Spotless Data',
      author_email='team@spotlessdata.com',
      license='MIT',
      packages=['pyspotless'],
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta',  # 5 - Production/Stable
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4'],
      keywords='spotless datacleansing',)
