from setuptools import setup

setup(
    name='djangorestframework-amauth',
    version='1.0',
    packages=['rest_framework_am_auth'],
    url='',
    license='',
    author='GS Labs',
    author_email='',
    description='AccountManager auth backend for DRF.',
    install_requires=(
        'Django',
        'djangorestframework',
        'requests_oauthlib',
    )
)
