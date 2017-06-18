from setuptools import setup

setup(
    name='pyintralinks',
    version='0.1.0',
    description='A python client for intralinks api.',
    long_description='Simplifies the use of Intralinks API.',
    url='https://github.com/delciotorres/pyintralinks',
    author='Delcio Torres',
    author_email='delciotorres@gmail.com',
    license='MIT',
    zip_safe=False,
    install_requires=['requests'],
    keywords=['intralinks', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: File Sharing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
