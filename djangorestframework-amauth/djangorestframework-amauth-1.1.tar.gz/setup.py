from setuptools import setup, find_packages

setup(
    name='djangorestframework-amauth',
    version='1.1',
    packages=find_packages(),
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
