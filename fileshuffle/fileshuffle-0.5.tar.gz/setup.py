from distutils.core import setup

with open('README.rst') as readme:
    long_description = readme.read()

VERSION = '0.5'

setup(
    install_requires=['tqdm'],
    name='fileshuffle',
    version=VERSION,
    py_modules=['fileshuffle'],
    url='https://github.com/sashgorokhov/fileshuffle',
    download_url='https://github.com/sashgorokhov/fileshuffle/archive/v%s.zip' % VERSION,
    keywords=['shuffle', 'file shuffle', 'filesystem'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia',
        'Topic :: System :: Filesystems'
    ],
    long_description=long_description,
    license='MIT License',
    author='sashgorokhov',
    author_email='sashgorokhov@gmail.com',
    description='Shuffle files',
    scripts=[
        'fileshuffle.py'
    ]
)
