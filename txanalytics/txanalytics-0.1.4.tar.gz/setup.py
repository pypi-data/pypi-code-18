from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Framework :: Twisted',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='txanalytics',
    packages=['txanalytics'],
    version='0.1.4',
    description='A Twisted based client for Google Analytics Measurement Protocol',
    author='Yehuda Deutsch',
    author_email='yeh@uda.co.il',
    license='MIT',
    install_requires=['treq', 'attrs'],
    url='https://gitlab.com/syncmeapp/txanalytics',
    download_url='https://gitlab.com/syncmeapp/txanalytics/repository/archive.tar.gz?ref=master',
    keywords=['analytics'],
    classifiers=CLASSIFIERS,
    platforms=['any'],
)
