from setuptools import setup

setup(
    name='AaronOS_Messaging',
    version='0.1.1',
    description='A command line client for the messaging app in Aaron OS',
    url='https://github.com/edison-moreland/AaronOS-Messaging-Client',
    download_url='https://github.com/edison-moreland/AaronOS-Messaging-Client/archive/0.1.1.tar.gz',
    author='Edison Moreland',
    author_email='edison@devdude.net',
    license='MIT',
    packages=['messaging_client'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'messaging = messaging_client.main:start'
        ]
    }
    )