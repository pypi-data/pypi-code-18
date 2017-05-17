from .constants import VOLUME_MODES


class ResultImage(object):
    """
    Represent final image built by incubator.
    """

    def __init__(self, image_id, logs=None):
        self._id = image_id
        self._logs = logs or []

    @property
    def id(self):
        return self._id

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)

    def __str__(self):
        return "ResultImage<id: {}>".format(str(self._id))


class CommandLog(object):
    """
    Represent logs for one dockerfile command.
    """

    def __init__(self, command, logs=None):
        self._command = command
        self._logs = logs or []

    @property
    def command(self):
        return self._command

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)

    def add_logs(self, logs):
        self._logs += logs


class Volume(object):
    """
    Representing a mount volume.
    """

    def __init__(self, source, destination, mode=None):
        self.source = source
        self.destination = destination
        self.mode = mode

    @staticmethod
    def get_instance(value):
        """
        Try to create a new Volume instance.

        :param value: Volume instance or string in the format source:destination or source:destination:mode
        :return: Volume instance when the input is valid, else raises an ValueError
        """
        if not value:
            raise ValueError("None cannot be converted to the Volume instance.")

        if isinstance(value, Volume):
            return value

        value_split = value.split(':')
        if len(value_split) == 2:
            source, destination = value_split
            mode = None
        elif len(value_split) == 3:
            source, destination, mode = value_split
            if not mode:
                raise ValueError(
                    "{} is not a valid volume in format "
                    "'source:destination' or 'source:destination:mode'."
                    "('source' and 'destination' should be nonempty)".format(
                        value))
        else:
            raise ValueError(
                "{} is not a valid volume in format "
                "'source:destination' or 'source:destination:mode'.".format(value))

        if not source or not destination:
            raise ValueError(
                "{} is not a valid volume in format "
                "'source:destination' or 'source:destination:mode'."
                "('source' and 'destination' should be nonempty)".format(
                    value))

        if mode and mode not in VOLUME_MODES:
            raise ValueError("{} is not a valid mode for volume. "
                             "(valid modes: {})".format(mode, VOLUME_MODES))

        return Volume(source=source,
                      destination=destination,
                      mode=mode)

    @staticmethod
    def get_instances(value_list):
        """
        Try to get list of Volume instances from the list.

        :return: list of valid Volume instances or raise a ValueError
        """
        return [Volume.get_instance(v) for v in value_list] if value_list else None

    def __str__(self):
        result = "{}:{}".format(self.source, self.destination)
        if self.mode:
            result += ":{}".format(self.mode)
        return result

    def __eq__(self, o):
        if not isinstance(o, Volume):
            return False

        return self.source == o.source and self.destination == o.destination and self.mode == o.mode

    def __hash__(self):
        result = (self.source.__hash__() ** 2) * self.destination.__hash__()
        if self.mode:
            result *= self.mode.__hash__() ** 3
        return int(result)

    @staticmethod
    def volumes_to_list(volumes):
        return [str(v) for v in volumes]

    @staticmethod
    def volumes_to_bind_dict(volumes):
        result = {}
        for v in volumes:
            result[v.source] = {
                "bind": v.destination,
                "mode": v.mode
            }
        return result
