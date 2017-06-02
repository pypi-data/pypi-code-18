from setuptools import setup, find_packages

setup(
    name='pubsub.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.1.0',
    description='Python PubSub Adapters for gcloud,redis and kafka',
    url='https://github.com/Superbalist/python-pubsub',
    install_requires=[
        'confluent-kafka',
        'google.cloud',
        'redis',
    ],
    test_requires=[
        'pytest-timeout'
    ],
    packages=find_packages(),
    zip_safe=False)
