from setuptools import setup, find_packages
from helga_amazon_meta import __version__ as version


setup(
    name='helga-amazon-meta',
    version=version,
    description=('Provide information for related metadata'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat :: Internet Relay Chat'],
    keywords='irc bot amazon-meta',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/helga-amazon-meta',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['helga_amazon_meta.plugin'],
    zip_safe=True,
    install_requires=[
        'helga',
        'python-amazon-simple-product-api',
    ],
    test_suite='',
    entry_points=dict(
        helga_plugins=[
            'amazon-meta = helga_amazon_meta.plugin:amazon_meta',
        ],
    ),
)
