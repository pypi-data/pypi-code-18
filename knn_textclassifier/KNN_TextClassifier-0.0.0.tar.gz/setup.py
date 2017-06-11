#coding:utf-8
'''
Created on 2017Äê6ÔÂ10ÈÕ

@author: Arnold_Gaius
'''

from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
  
setup(  
    name="KNN_TextClassifier",  
    version="0.0.0",  
    author="Arnold_Gaius",  
    author_email="jiangcmd@qq.com",  
    description="KNN_TextClassifier",  
    long_description=LONG_DESCRIPTION,  
    license="BSD",  
    url="https://github.com/ArnoldGaius/KNN_TextClassifier",  
    packages=['src'],  
    install_requires=[   
        "numpy",
        ],  
    classifiers=[  
        "Programming Language :: Python",  
        "Programming Language :: Python :: 2",    
        "Programming Language :: Python :: 2.7",  
    ],  
)  