from setuptools import setup, find_packages

setup(name='twitter_controller',
      version='0.8',
      description='This is a package to analyze tweets of a certain person',
      url='https://github.com/AGHPythonCourse2017/zad3-kanes115.git',
      author='Dominik Stanaszek',
      author_email='dominikstanaszek@icloud.com',
      license='NONE',
      packages=find_packages(),
      package_data={'': ['twitter_controller/resources/*']},
      include_package_data=True,
      install_requires=[
        'numpy',
        'indicoio',
        'pytest'
      ],
      zip_safe=False)