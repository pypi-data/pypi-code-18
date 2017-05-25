from distutils.core import setup


setup(
    name='thingface-client',
    packages=['thingface'],
    version='0.2',
    description='Thingface gateway client module',
    author='gebri',
    author_email='gebri@inmail.sk',
    url='https://github.com/thingface/python',
    keywords=['thingface'],
    install_requires=['paho-mqtt>=1.2'],
    classifiers=['Development Status :: 3 - Alpha'],
    package_data={
        'thingface': ['ca.crt'],
    },
)
