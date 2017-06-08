#coding:utf-8
'''
Created on 2017Äê6ÔÂ8ÈÕ

@author: Arnold_Gaius,ChiangClaire
'''

from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
  
setup(  
    name="Tf-Idf-CategoryWeighting",  
    version="0.0.0",  
    author="Arnold_Gaius,ChiangClaire",  
    author_email="jiangcmd@qq.com",  
    description="Tf-Idf-CategoryWeighting",  
    long_description=LONG_DESCRIPTION,  
    license="BSD",  
    url="https://github.com/ArnoldGaius/Tf-idf-Category-weighting-transformer",  
    packages=['Tf-Idf-CategoryWeighting'],  
    install_requires=[  
        "scikit-learn",  
        "numpy",
        "scipy",
        ],  
    classifiers=[  
        "Programming Language :: Python",  
        "Programming Language :: Python :: 2",    
        "Programming Language :: Python :: 2.7",  
    ],  
)  