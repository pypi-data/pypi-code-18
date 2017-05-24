from setuptools import setup, find_packages
import os


setup(name='baselines',
      packages=[package for package in find_packages()
                if package.startswith('baselines')],
      install_requires=[
          'scipy',
          'tqdm',
          'joblib',
          'zmq',
          'dill',
          'tensorflow >= 1.0.0',
          'azure==1.0.3',
          'progressbar2',
      ],
      description="OpenAI baselines: high quality implementations of reinforcement learning algorithms",
      author="OpenAI",
      url='https://github.com/openai/baselines',
      author_email="gym@openai.com",
      version="0.1.1")
