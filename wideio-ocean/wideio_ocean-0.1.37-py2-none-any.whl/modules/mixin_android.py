import os


class MixIn(object):
    """ Add support for android development from docker """

    @classmethod
    def android_compat(cls):
        """
        Setup the system to allow android SDK to work from within container
        """
        os.system('sudo /bin/bash -c "echo 1> /sys/module/usbcore/parameters/old_scheme_first"')
