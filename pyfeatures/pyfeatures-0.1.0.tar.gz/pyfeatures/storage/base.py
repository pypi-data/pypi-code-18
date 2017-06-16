
class FeatureStorage(object):
    """
    Base class for feature storages, which are used to read or persist feature
    data.
    """

    def get_feature_by_name(self, feature_name):
        """
        Get feature data for the feature named `feature_name`

        :param feature_name: The name of the feature.
        :return: Feature object containing the feature data or None if the feature doesn't exist.
        """
        raise NotImplementedError()

    def set_feature(self, feature):
        """
        Save a feature.

        :param feature: Feature object containing the feature data.
        """
        raise NotImplementedError()


class User(object):
    """
    The base class for all users that go through this system.
    """

    def get_id(self):
        """
        Gets the ID of the user.

        :return: The id of the user. Usually an int or str.
        """
        raise NotImplementedError()

    def is_in_groups(self, groups):
        """
        Checks whether the user is in the given groups.

        :param groups: A list of str group names.
        :return: True if the user is in at least one of those groups, otherwise False
        """
        raise NotImplementedError()
