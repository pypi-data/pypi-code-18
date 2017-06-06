from setuptools import setup, find_packages


setup(
    name='maas',
    version='0.0.3',
    url='https://gitlab.com/matix-io/django-maas',
    license='BSD',
    description='Django wrapper for interfacing with e-Mail as a Service providers.',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',  # SEE NOTE BELOW (*)
    packages=find_packages(),
    install_requires=[],
    zip_safe=False,
    classifiers=[]
)