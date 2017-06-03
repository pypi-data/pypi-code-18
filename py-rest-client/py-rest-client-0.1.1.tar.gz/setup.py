# -*- coding: utf-8 -*-
from distutils.core import setup

try:
    with open('README.md', 'r') as f:
        readme = f.read()

    with open('LICENSE.txt', 'r') as f:
        license_ = f.read()
except:
    readme = ''
    license_ = ''


setup(
    name='py-rest-client',
    version='0.1.1',
    packages=['rest_client', 'rest_client.lib', 'rest_client.lib.utils'],
    url='',
    download_url='https://github.com/slawek87/py-rest-client',
    license=license_,
    author='Sławomir Kabik',
    author_email='slawek@redsoftware.pl',
    description='Py-Rest-Client is a useful lib for programmers who work with clients for REST API. '
                'In simply and easy way you can build Endpoint classes where you put endpoint settings.'
                'In that case you have clean structure of endpoints in your code. '
                'This lib is only for consume REST API endpoints.',
    long_description=readme,
    keywords=['rest api client', 'python rest api client', 'rest api endpoint', 'consume rest api'],
    install_requires=['setuptools', 'requests', 'requests_oauthlib']
)
