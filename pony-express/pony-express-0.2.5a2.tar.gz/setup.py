#!/usr/bin/env python

from setuptools import setup

setup(	name='pony-express',
        license = "LGPL-3",
        version='0.2.5.a2',
        description='General purpose package and dependency manager based on MongoDB',
        long_description="""
Artifact PonyExpress (or simply Pony) is an artifact repository and package manager that aims to simplify software modules integration into big projects. It is designed with native (read modern C++) development in mind but it is usefull everywhere there is an environment to setup in order to transform versioned data using any software.

Note: As pony works well with binary components, the transformation function (the tool used to transform data) itself may be a packaged component.

Pony use MongoDB as backend to store your packages and meta-informations so a running local or remote MongoDB database is needed in order to use pony. The pony's MongoDB database is the **pony_store** and the only collection it uses as a repository is named **packages**.

You can perform two main operation from the pony command line:
  
  - **charge** the pony to deliver your artifact to clients.
  - **deliver** dependencies of the working artifact to users.
""",
        author='Giuseppe Puoti',
        author_email='giuseppe.puoti@gmail.com',
        url='https://github.com/gpuoti/Artifact-PonyExpress',

        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Software Development :: Version Control",
            "Topic :: System :: Archiving :: Packaging",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        ],
        
        py_modules=[
            'pony', 
            'bag',
            'config_constrainer',
            'dependencies',
            'alternative_set',

            'pony_scons',
            'cli'
            # list them here when you add any other modules!
            ],
            
        
        
        install_requires = [
            'tabulate', 
            'colorama', 
            'networkx',
            'pymongo'
            # add any other dependency package here in order to let pip install them as installation' side effect.
            ],
            
        scripts = ['pony.py']  
)