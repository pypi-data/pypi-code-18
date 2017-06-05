#coding:utf-8
'''
Created on 2017Äê6ÔÂ5ÈÕ

@author: Arnold_Gaius,ChiangClaire
'''

from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
  
setup(  
    name="TextClassifier",  
    version="0.0.6",  
    author="Arnold_Gaius,ChiangClaire",  
    author_email="jiangcmd@qq.com",  
    description="Short text Classifier based on Numpy,scikit-learn,Pandas,Matplotlib",  
    long_description=LONG_DESCRIPTION,  
    license="MIT",  
    url="https://github.com/ArnoldGaius/Text_Classifier",  
    packages=['TextClassifier'],  
    install_requires=[  
        "scikit-learn",  
        "numpy",
        "matplotlib",
        "pandas",
        ],  
    classifiers=[  
        "Programming Language :: Python",  
        "Programming Language :: Python :: 2",    
        "Programming Language :: Python :: 2.7",  
    ],  
)  