from setuptools import setup, find_packages


setup(
    name='awesome-django-admin-locking',
    version='1.3',
    url='https://github.com/ndanielsen/Awesome-Django-Admin-Locking',
    download_url='https://github.com/ndanielsen/Awesome-Django-Admin-Locking/archive/1.3.tar.gz3',
    license='BSD',
    description='Prevents users from overwriting each others changes in Django. Forked from JoshMaker for upload to pypi.',
    author='Josh West',
    packages=find_packages(),
    install_requires=[],
    zip_safe=False,
    keywords=['Awesome', 'Django', 'admin', 'locking'],
    classifiers=[]
)
