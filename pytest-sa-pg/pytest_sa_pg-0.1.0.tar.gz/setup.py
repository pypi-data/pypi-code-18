from setuptools import setup

description = """
pytest_sa_pg provides basic support to create, start/stop
postgres clusters for unit tests using pytest and sqlalchemy
"""

setup(name='pytest_sa_pg',
      version='0.1.0',
      description=description,
      author='Aurélien Campéas',
      author_email='aurelien.campeas@pythonian.fr',
      url='https://bitbucket.org/pythonian/pytest_sa_pg',
      license='LGPL',

      packages=['pytest_sa_pg'],
      package_dir={'pytest_sa_pg': '.'},
      install_requires=[
          'psycopg2',
          'sqlalchemy',
      ],
)
