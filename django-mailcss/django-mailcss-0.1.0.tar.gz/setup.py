from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements/requirements-mandatory.txt").readlines()]

setup(
    name='django-mailcss',
    version="0.1.0",
    description='A Django app useful for inlining CSS (primarily for e-mails)',
    long_description=open('README.md').read(),
    author='contact@jhink.com',
    author_email='contact@jhink.com',
    maintainer='Ch Ray',
    maintainer_email='ray@jhink.com',
    license='BSD',
    url='https://github.com/wejhink/django-mailcss',
    download_url='https://github.com/wejhink/django-mailcss/releases',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['html', 'css', 'inline', 'style', 'email'],
    classifiers=[
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    install_requires=REQUIREMENTS,
)
