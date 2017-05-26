from setuptools import setup, find_packages

setup(
    name = 's_sqlachemy',
    version = '0.1',
    keywords = ('s_sqlachemy', 'orm'),
    description = '',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
    license = 'MIT License',
    install_requires = ['SQLAlchemy>=1.1.9'],

    author = 'shennian',
    author_email = 'ashen19@hotmail.com',

    packages = find_packages(),
    platforms = 'any',
)
