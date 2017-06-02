from setuptools import setup, find_packages

setup(
    name='hackintosh',
    version='0.1',
    packages=find_packages(),
    author = 'Gary Niu',
    author_email = 'gary.niu@gmail.com',
    url = 'https://github.com/yekki/hackintosh',
    keywords = ['hackintosh', 'macos', 'osx'],
    include_package_data=True,
    classifiers = [],
    install_requires=[
        'click','beautifulsoup4', 'requests'
    ],
    entry_points='''
        [console_scripts]
        yekki=hackintosh.main:cli
    ''',
)