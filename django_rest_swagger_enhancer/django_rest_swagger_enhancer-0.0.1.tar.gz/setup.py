from setuptools import find_packages, setup
# Read more here: https://www.codementor.io/arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku

setup(
    name='django_rest_swagger_enhancer',
    packages=find_packages(),
    include_package_data=True,
    version='0.0.1',
    description='A basic logger for Django',
    author='Eshan Das',
    author_email='eshandasnit@gmail.com',
    url='https://github.com/eshandas/django_rest_swagger_enhancer',  # use the URL to the github repo
    download_url='https://github.com/eshandas/django_rest_swagger_enhancer/archive/0.0.1.tar.gz',  # Create a tag in github
    keywords=['django', 'django rest framework', 'swagger', 'django rest swagger'],
    classifiers=[],
)
