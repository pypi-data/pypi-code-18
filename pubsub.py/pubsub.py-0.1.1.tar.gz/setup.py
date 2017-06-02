from setuptools import setup, find_packages

setup(
    name='pubsub.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.1.1',
    description='Python PubSub Adapter for gcloud',
    url='https://github.com/Superbalist/python-pubsub',
    install_requires=[
        'google-cloud-pubsub',
    ],
    test_requires=[
        'pytest-timeout'
    ],
    packages=find_packages(),
    zip_safe=False)
