#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 17:23:33 2017

@author: aidanrocke
"""

from sklearn.preprocessing import StandardScaler


def preprocess_data(X, scaler=None):
    if not scaler:
        scaler = StandardScaler()
        scaler.fit(X)
    X = scaler.transform(X)
    return X, scaler