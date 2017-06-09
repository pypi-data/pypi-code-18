from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ternpy',
      version='0.1',
      long_description=readme(),
      description='Ternary Plot Tool',
      url='http://github.com/ad1v7/ternpy',
      author='Marcin Kirsz',
      author_email='marcin.kirsz@example.com',
      license='MIT',
      packages=['ternpy'],
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
