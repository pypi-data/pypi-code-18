# from setuptools import setup
from distutils.core import setup

PACKAGE_NAME = "es_wrapper"

packages = [
  PACKAGE_NAME,
  ]

install_requires = ['elasticsearch', 'jsonpickle', "pytz", "logstash_formatter"
    ]

long_desc = """A wrapper for Elasticsearch"""

import es_wrapper
version = es_wrapper.__version__

setup(name=PACKAGE_NAME,
      version=version,
      description="A wrapper package for easy Elasticsearch Interface",
      long_description=long_desc,
      author="Guy Eshet",
      author_email="guyeshet@gmail.com",
      url="https://github.com/guyeshet/eswrapper.git",
      install_requires=install_requires,
      packages=packages,
      package_data={},
      license="Apache 2.0",
      keywords="elasticsearch",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: POSIX',
                   'Topic :: Internet :: WWW/HTTP'])
