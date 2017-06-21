from setuptools import setup, find_packages

setup(
    name='awslambdahelper',
    version='0.0.2',
    install_requires=['boto3'],
    setup_requires=['pytest-runner','twine'],
    tests_require=['pytest', 'pytest-mock','moto'],
    description='Handlers the nasty bits of AWS config rules',
    url='http://github.com/drewsonne/awslambdahelper',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    license='GLPG',
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "lambdahelper-bundle=awslambdahelper.cli:main",
        ],
    },
)
