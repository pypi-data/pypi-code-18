import re


class MixIn(object):
    """
    Various commands to make tests easier.
    """

    @classmethod
    def tdd(cls, srv=None, *options):
        """
        Run unit tests by running pytest inside of the container.
        """
        if srv is None or srv == "-a":
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    cls.tdd(s)
            return
        desc = cls._ocean._get(srv)
        success, return_code = cls._ocean.shell(srv, "-n", "tdd", command=desc.get("tdd-command", "/bin/bash -c 'py.test'"))
        return success, return_code

    @classmethod
    def unit(cls, srv=None, *options):
        return cls.tdd(srv, *options)

    @classmethod
    def bdd(cls, srv=None, *options):
        """
        Run unit tests by running pytest inside of the container.
        """
        if srv is None or srv == "-a":
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    cls.tdd(s)
            return
        desc = cls._ocean._get(srv)
        return cls._ocean.shell(srv, "-n", "bdd", command=desc.get("bdd-command", "/bin/bash -c 'behave'"))

    @classmethod
    def bdd_spec(cls, srv, *options):
        """
        Run behave tests in the container.
        """
        cls.restart(srv)
        desc = cls._ocean._get(srv)
        return cls._ocean.shell(desc.get("bdd-repo", "bdd"), "-al",
                                command=desc.get("bdd-spec-command",
                                                 "/bin/bash -c 'behave -v --junit --junit-directory reports tests/api/%s "
                                                 " --tags ~@notimplemented %s'") % (
            re.sub("[0-9-]", "", srv), " ".join(options)))
