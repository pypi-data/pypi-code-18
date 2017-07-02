#
# Flask-Chargebee
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from setuptools import find_packages, setup


setup(
    name='Flask-Chargebee',
    version='0.0.1',
    description='Flask-Chargebee',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-chargebee',
    install_requires=('flask', 'chargebee', 'six'),
    packages=find_packages(),
)


# EOF
