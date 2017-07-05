from setuptools import find_packages, setup


setup(name='cyberglove',
      version='0.1.32',
      description='Communicate with cyberglove from python',
      packages=find_packages(),
      author='Alex Ray',
      author_email='aray@openai.com',
      install_requires=['numpy>=1.12.1', 'pyserial>=3.3', 'mujoco_py>=1.50.0.0'],
      include_package_data=True)
