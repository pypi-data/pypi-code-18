from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='TbaApi3',
      version='0.1a3',
      description='A Python library for the TBA API v3',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
      ],
      url='https://github.com/DanWaxman/TbaApi3',
      author='Dan Waxman',
      author_email='dan.waxman1@gmail.com',
      license='MIT',
      packages=['TbaApi3'],
      install_requires=[
        'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)