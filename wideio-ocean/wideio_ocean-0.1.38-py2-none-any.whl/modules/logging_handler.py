
class LoggingHandler(object):
    @classmethod
    def on_ocean_start(cls, ocean):
        cls._ocean = ocean

    @classmethod
    def _dockerenv_options(cls, section, srv, r):
        if cls._ocean._get_config("WITH_FLUENT"):
            return r + ["--log-driver=fluentd", "--log-opt fluentd-address=" + cls._ocean._get_config("WITH_FLUENT")]
        else:
            return r


__handler__ = LoggingHandler
