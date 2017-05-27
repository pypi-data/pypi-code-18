#
# Flask-Keen
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from setuptools import find_packages, setup


setup(
    name='Flask-BDEA',
    version='0.1.0',
    description='Flask-BDEA',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-bdea',
    install_requires=('flask', 'block-disposable-email'),
    packages=find_packages(),
)


# EOF
