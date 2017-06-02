from setuptools import setup, find_packages

setup(
    name='pubsub-validators.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.1.0',
    description='Python PubSub Validators  for gcloud, redis and kafka',
    url='https://github.com/Superbalist/python-pubsub-validators',
    install_requires=[
        'jsonschema',
    ],
    packages=find_packages(),
    zip_safe=False)
