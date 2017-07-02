from setuptools import setup, find_packages
import re

with open("requirements.txt") as f:
  requirements = f.read().splitlines()

with open("nexus_stats/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Version is not set")

setup(name="nexus-stats.py",
      author="Orangutan",
      author_email="nihaal.s@live.co.uk",
      url="https://github.com/OrangutanGaming/Nexus-Stats-py",
      version=version,
      # package_dir={"": "nexus-stats"},
      packages=find_packages(),
      license="MIT",
      description="A python module for the Nexus Stats API",
      include_package_data=True,
      install_requires=requirements,
      classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
      ]
)