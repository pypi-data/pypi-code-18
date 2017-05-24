from setuptools import setup, find_packages

setup(
    name='lndrpc',
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'grpcio_tools',
        'googleapis-common-protos'
    ],
    include_package_data=True,
)
