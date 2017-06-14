from setuptools import setup, find_packages

install_requires = ['requests', 'beautifulsoup4']
test_require = ['pytest', 'flake8']

setup(name='californiasos',
      version='0.1.1',
      description='Python bindings to the California SOS Business Entity Search',
      url='https://github.com/jacobgreenleaf/californiasos',
      author='Jacob Greenleaf',
      author_email='jacob@jacobgreenleaf.com',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      tests_require=test_require,
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 3',
                   'Topic :: Internet :: WWW/HTTP',
                   'License :: OSI Approved :: MIT License'])
