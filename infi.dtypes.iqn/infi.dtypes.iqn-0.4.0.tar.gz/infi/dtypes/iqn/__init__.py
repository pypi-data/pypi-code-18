class InvalidIQN(ValueError):
    def __init__(self, name):
        super(InvalidIQN, self).__init__('Invalid IQN {}'.format(name))


class iSCSIName(object):
    def __init__(self, name):
        super(iSCSIName, self).__init__()
        self._name = name._name if isinstance(name, iSCSIName) else name.lower() # pylint: disable=protected-access

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        if not isinstance(other, iSCSIName):
            try:
                other = iSCSIName(other)
            except Exception:  # pylint: disable=broad-except
                return False
        return self._name == other._name  # pylint: disable=protected-access

    def __ne__(self, other):
        return not (self == other)  # pylint: disable=superfluous-parens


class IQN(iSCSIName):
    def __init__(self, name):
        super(IQN, self).__init__(name)
        fields = self._name.split(':')
        base, self._extra = fields[0], tuple(fields[1:])
        base_fields = base.split('.')
        if len(base_fields) < 2:
            raise InvalidIQN(name)
        self._type = base_fields[0]
        self._date = base_fields[1]
        self._naming_authority = '.'.join(base_fields[2:])
        if self._type != 'iqn':
            raise InvalidIQN(name)

    def get_date(self):
        return self._date

    def get_naming_authority(self):
        return self._naming_authority

    def get_extra(self):
        return ':'.join(self._extra)

    def get_extra_fields(self):
        return self._extra


def make_iscsi_name(iscsi_name):
    try:
        return IQN(iscsi_name)
    except InvalidIQN:
        return iSCSIName(iscsi_name)
