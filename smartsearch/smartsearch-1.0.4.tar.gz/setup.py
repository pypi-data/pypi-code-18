from setuptools import setup
from pip.req import parse_requirements
import uuid

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=uuid.uuid1())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='smartsearch',
      version='1.0.4',
      description='A module that searches various internet sources to find direct answers to queries.',
      url='https://github.com/ironman5366/smartsearch',
      author='Will Beddow',
      author_email='will@willbeddow.com',
      license='MIT',
      packages=['smartsearch'],
      zip_safe=False, install_requires=reqs)

