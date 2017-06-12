from setuptools import setup

setup(name='linearcorex',
      version='0.5',
      description='Linear CorEx finds latent factors that explain relationships in data.',
      url='http://github.com/gregversteeg/linearcorex',
      author='Greg Ver Steeg',
      author_email='gversteeg@gmail.com',
      license='AGPL-3.0',
      packages=['linearcorex'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'seaborn', 'networkx'],
      zip_safe=False)
