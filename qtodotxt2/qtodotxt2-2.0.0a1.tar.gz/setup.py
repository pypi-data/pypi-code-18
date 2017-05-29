from setuptools import setup, find_packages

import sys


setup(name="qtodotxt2", 
      version="2.0.0a1",
      description="Cross Platform todo.txt GUI",
      author="QTT Development Team",
      author_email="qtodotxt@googlegroups.com",
      url='https://github.com/QTodoTxt/QTodoTxt2',
      packages=find_packages(include=("*.qml")),
      provides=["qtodotxt2"],
      depends=["python-dateutil"],
      license="GNU General Public License v3 or later",
      #install_requires=install_requires,
      classifiers=["Environment :: X11 Applications :: Qt",
                   "Programming Language :: Python :: 3",
                   "Intended Audience :: End Users/Desktop",
                   "Operating System :: OS Independent",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
                   ],
      entry_points={'console_scripts': 
                    [
                        'qtodotxt2 = qtodotxt.app:run'
                    ]
                    }
      )

