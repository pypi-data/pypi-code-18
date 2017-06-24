# IMPORTS
from utils import getType
import csv
import numpy as np
import random

# SAMPLE


class Sample(object):

    def __init__(self, features, label, featureFilter=None):
        # Label is INT
        # Feature vector is float
        width = len(features)
        self.label = label
        self.prediction = 0
        self.support = None
        self.featureFilter = featureFilter

        # Missing values are None
        for index, value in enumerate(features):
            if value == '?':
                features[index] = None

        self.features = np.array(features).astype(np.float)

    def setFeatureFilter(self, featureFilter):
        self.featureFilter = featureFilter

    def decidePrediction(self):
        self.prediction = np.argmax(self.support)

    def getFeatures(self):
        if self.featureFilter is None:
            return self.features
        else:
            return self.features[self.featureFilter]
