
import uuid
import zlib

ALL = "ALL"
NONE = "NONE"


class Feature(object):

    def __init__(self, name, *, users=None, groups=None, percentage=None,
                 randomize=False):
        """
        A representation of a feature for use in PyRollout.

        :param name: Name of the feature. This is what you will pass in when checking the access.
        :param users: A list of user IDs that should have access.
        :param groups: A list of group names to which access is allowed. "ALL" and "NONE" are special names.
        :param percentage: A percentage of the user base that should receive access to this feature. See can_percentage
        :param randomize: Whether or not the percentage should be kind of randomized. Default: False
        """
        self.name = name
        self.users = users if users is not None else []
        self.groups = groups if groups is not None else []
        if ALL in self.groups:
            assert NONE not in self.groups
        self.percentage = percentage
        self.randomize = randomize

    def __repr__(self):
        """
        Build Feature representation.

        :returns: str repr: ``eval``-ready string representation of feature.
        """
        s = []
        if self.name:
            s.append("'%s'" % self.name)

        for p in ['groups', 'users']:
            v = getattr(self, p)
            s.append('%s=%s' % (p, repr(v)))
            s = ', '.join(s)
            return 'Feature(%s)' % s

    def __str__(self):
        """
        Nicer representation of feature with semi-readable configuration.

        :returns: str str: Human-readable string representation of feature.
        """
        repr_string = '<Feature {NAME} - %s>'.format(NAME=self.name)
        config_string = ''

        if len(self.users) > 0:
            config_string += 'Users:%s ' % self.users

        if len(self.groups) > 0:
            config_string += 'Groups:%s ' % self.groups

        return repr_string % config_string.strip()

    def can(self, user):
        """
        Check if the user can access this feature.

        :param user: Object representing the user and implementing pyrollout.storage.User
        :return: True if user can access the feature, otherwise False
        """
        if self.can_user(user):
            return True
        elif self.can_group(user):
            return True
        elif self.can_percentage(user):
            return True
        else:
            return False

    def can_group(self, user):
        """
        Check if user can access feature by group.

        :param user: Object representing the user and implementing pyrollout.storage.User
        :return: True if user can access the feature, otherwise False
        """
        if ALL in self.groups:
            return True
        elif NONE in self.groups:
            return False
        else:
            return user.is_in_groups(self.groups)

    def can_user(self, user):
        """
        Check if user can access feature by its user id.

        :param user: Object representing the user and implementing pyrollout.storage.User
        :return: True if user can access the feature, otherwise False
        """
        return user.get_id() in self.users

    def can_percentage(self, user):
        """
        Check if user can access feature by percentage.

        Works best with sequential ids and >100 users.

        :param user: Object representing the user and implementing pyrollout.storage.User
        :return: True if user can access the feature, otherwise False
        """
        if self.percentage is None:
            return False

        user_id = user.get_id()
        assert isinstance(user_id, int) or isinstance(user_id, uuid.UUID) or isinstance(user_id, str)

        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        if isinstance(user_id, uuid.UUID):
            user_id = user_id.int

        if self.randomize:
            user_id += zlib.crc32(bytes(self.name.encode("utf-8")))

        return user_id % 100 < self.percentage
