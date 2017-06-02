import os


class NetworkAttachHandler(object):
    """
    Allow to attach network to more than one on start.
    Note there is a slight delay for containers joining the networks.
    It is due to current docker limitation allowing only one network to be specified at launch.
    """

    @classmethod
    def on_ocean_start(cls, ocean):
        cls._ocean = ocean

    @classmethod
    def on_post_start(cls, name, *args):
        if cls._ocean._get_config("docker.extra_network"):
            cls.attach_extra_network(name, *args)

    @classmethod
    def attach_extra_network(cls, name, *args):
        netname = cls._ocean._get_config("docker.extra_network")
        netopts = cls._ocean._get_config("docker.extra_network_opts", "")
        netprefix = cls._ocean._get_config("docker.extra_network_host_prefix",
                                           (os.uname()[1] + "/" if len(netopts) else ""))
        cls._ocean._subprocess_popen("docker %s network connect %s %s%s --alias=%s.%s" % (netopts, netname, netprefix, name,
                                                                                          name, netname)).communicate()


__handler__ = NetworkAttachHandler
