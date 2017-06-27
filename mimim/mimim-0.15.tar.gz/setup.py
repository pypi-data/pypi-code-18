from setuptools import setup


setup(
    name='mimim',
    packages=['vision'],
    version='0.15',
    description='An upload to s3 utility',
    author='Fathom',
    author_email='mirabel.ekwenugo@andela.com',
    keywords=['upload', 'files', 's3'],
    classifiers=[],
    install_requires=[
        'requests==2.13.0',
        'appdirs==1.4.3',
        'boto==2.46.1',
        'click==6.7',
        'cx-Freeze==5.0.1',
        'Flask==0.12',
        'Gooey==0.9.2.3',
        'itsdangerous==0.24',
        'mock==2.0.0',
        'nose==1.3.7',
        'packaging==16.8',
        'PyInstaller==3.2.1',
        'pypref==2.0.0',
        'six==1.10.0',
        'watchdog==0.8.3',
        'Werkzeug==0.12',
    ],
)
