

class Manager(object):

    def __init__(self, *, feature_storage=None, undefined_feature_access=False):
        """
        Manages feature flags for groups, users, or on a percentage basis. This
        uses pluggable persistence so that there's no dependecy on any specific
        persistence mechanism.

        :param feature_storage: Object to manage storage of feature definitions
        :param undefined_feature_access: Should undefined features be allowed (default:True) or denied (False) access?
        """
        if feature_storage is None:
            from pyfeatures.storage.memory import MemoryStorage
            self.feature_storage = MemoryStorage()
        else:
            self.feature_storage = feature_storage

        self.undefined_feature_access = undefined_feature_access

    def can(self, user, feature_name):
        """
        Check whether a user has access to the given feature.

        :param user: The user object that implements pyfeatures.storage.User
        :param feature_name: Name of the feature to check if the user has access.
        :return: True if user has access, otherwise False
        """
        feature = self.feature_storage.get_feature_by_name(feature_name)
        if feature is None:
            return self.undefined_feature_access
        return feature.can(user)

    def set_feature(self, feature):
        """
        Add a feature to be handled by this manager.

        :param feature: New feature to add
        """
        self.feature_storage.set_feature(feature)
