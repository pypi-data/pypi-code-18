from setuptools import setup

setup(
    name='fiddler',
    version='0.4',
    py_modules=['pyfiddler','certificate'],
    install_requires=[
        'datetime',
        'pythonnet',
        'pypiwin32',
    ],
    data_files=[('.',['BCMakeCert.dll', 'CertMaker.dll', 'FiddlerCore4.dll'])],
    entry_points='''
        [console_scripts]
        long=pyfiddler:dant
    ''',
)
