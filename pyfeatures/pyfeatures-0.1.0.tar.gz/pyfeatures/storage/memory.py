
from .base import FeatureStorage


class MemoryStorage(FeatureStorage):

    def __init__(self):
        self.feature_data = {}

    def get_feature_by_name(self, feature_name):
        return self.feature_data.get(feature_name, None)

    def set_feature(self, feature):
        self.feature_data[feature.name] = feature
