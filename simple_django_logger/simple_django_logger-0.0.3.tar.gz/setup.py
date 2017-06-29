from distutils.core import setup


setup(
    name='simple_django_logger',
    packages=[
        'simple_django_logger',  # this must be the same as the name above
        'simple_django_logger.middleware',
        'simple_django_logger.migrations'],
    version='0.0.3',
    description='A basic logger for Django',
    author='Eshan Das',
    author_email='eshandasnit@gmail.com',
    url='https://github.com/eshandas/simple_django_logger',  # use the URL to the github repo
    download_url='https://github.com/eshandas/simple_django_logger/archive/0.0.3.tar.gz',  # Create a tag in github
    keywords=['django', 'logger'],
    classifiers=[],
)
