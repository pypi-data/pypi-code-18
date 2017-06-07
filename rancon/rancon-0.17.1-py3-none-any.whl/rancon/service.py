""" definition of a service """

import re

from dotmap import DotMap


class Service(DotMap):
    """ class representing a service """

    def __init__(self, name, host, port, source, **kwargs):
        super().__init__()

        self.name = name
        self.host = host
        self.port = port
        self.source = source
        self.update(kwargs)

        # replace all tags in all values
        for key, value in self.items():
            if isinstance(value, str):
                self[key] = re.sub("%([^%]+)%",
                                   lambda x: self.get(x.group(1).lower(),
                                                      "UNDEFINED"),
                                   value)

    def __str__(self):
        return "{} ({}:{})".format(
            self.name, self.host, self.port
        )
