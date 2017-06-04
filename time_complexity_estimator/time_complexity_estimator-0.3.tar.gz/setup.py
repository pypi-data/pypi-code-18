from setuptools import setup

with open('README.rst') as readme_file:
    long_description = readme_file.read()

setup(
    name='time_complexity_estimator',
    version='0.3',
    description='Estimate time complexity from execution time',
    author='Mieszko Makuch',
    author_email='mmakuch@googlemail.com',
    url='https://github.com/',
    license='LICENSE.txt',
    long_description=long_description,
    packages=['time_complexity_estimator'],
    install_requires=[
        "numpy==1.11.3",
        "scipy==0.18.1"
    ],
    zip_safe=False
)
