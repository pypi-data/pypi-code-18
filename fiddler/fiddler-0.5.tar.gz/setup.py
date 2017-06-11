from setuptools import setup

setup(
    name='fiddler',
    version='0.5',
    py_modules=['pyfiddler','certificate'],
    install_requires=[
        'datetime',

    ],
    data_files=[('.',['BCMakeCert.dll', 'CertMaker.dll', 'FiddlerCore4.dll'])],
    entry_points='''
        [console_scripts]
        long=pyfiddler:dant
    ''',
)
