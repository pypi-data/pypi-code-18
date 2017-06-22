#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 13:38:46 2017

@author: diezg@Inelta.local0,784
"""
### Based on u3allio.c
import u3
from datetime import datetime

chanels=[0,2,3]
numChannels = len(chanels)
quickSample = 1
longSettling = 0
latestAinValues = [0] * numChannels
numIterations = 1000


