""" sets up the base class for all source services """
from rancon.common import CommonBase


class SourceBase(CommonBase):
    """ base class for all implementations of a source """
    required_opts = ()
    additional_opts = ()

    def get_services(self, **kwargs):
        """ empty """
        pass
