from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sentry_logger',
      version='1.0',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Bug Tracking',
      ],
      description='Basic helper for logging function / class based errors to sentry.io',
      url='https://github.com/gurayinan/sentry_logger',
      author='Guray Inan',
      author_email='gurayinan@windowslive.com',
      license='MIT',
      packages=['sentry_logger'],
      install_requires=[
          'raven'
      ],
      zip_safe=False)
