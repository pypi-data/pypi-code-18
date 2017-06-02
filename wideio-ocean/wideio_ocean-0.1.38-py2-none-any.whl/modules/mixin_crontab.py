import hashlib
import os

# used by nginx, passwordreminders, static websites reconstruction (equity, kashflow, propsearch...)


class MixIn(object):
    """
    Manages a system crontab for the specified manifest file.
    """

    @classmethod
    def cron_register(cls):
        """Register for events from cron daemon."""
        cron_fn = cls._cron_fn()
        for p in ["hourly", "daily", "weekly", "monthly"]:
            open("/etc/cron." + p + "/" + cron_fn, "w").write((
                "#!/bin/bash\nexport OCEANPATH=%s\nexport "
                "OCEAN_MANIFEST=%s\nsudo -E -u %s ocean cron_run_" + p + "\n")
                % (cls._ocean.MP, cls._ocean.MANIFEST_PATH, cls._ocean._get_config("cron.user", "nobody"))
            )
            os.chmod("/etc/cron." + p + "/" + cron_fn, 0o755)

    @classmethod
    def _cron_fn(cls):
        cron_fn = "ocean-%s.cron.sh" % (hashlib.md5(cls._ocean.MP.encode('utf8')).hexdigest()[:16:2],)
        return cron_fn

    @classmethod
    def cron_unregister(cls):
        for p in ["hourly", "daily", "weekly", "monthly"]:
            os.unlink("/etc/cron." + p + "/" + cls._cron_fn())

    @classmethod
    def cron_run_hourly(cls):
        for section, srv in cls._ocean._all_services():
            srvd = cls._ocean._get(srv)
            if "cron" in srvd and "hourly" in srvd["cron"]:
                cmd = srvd["cron"]["hourly"]
                cls._ocean.shell(srv, "-c", cmd)

    @classmethod
    def cron_run_daily(cls):
        for section, srv in cls._ocean._all_services():
            srvd = cls._ocean._get(srv)
            if "cron" in srvd and "daily" in srvd["cron"]:
                cmd = srvd["cron"]["daily"]
                cls._ocean.shell(srv, "-c", cmd)

    @classmethod
    def cron_run_weekly(cls):
        for section, srv in cls._ocean._all_services():
            srvd = cls._ocean._get(srv)
            if "cron" in srvd and "weekly" in srvd["cron"]:
                cmd = srvd["cron"]["weekly"]
                cls._ocean.shell(srv, "-c", cmd)

    @classmethod
    def cron_run_monthly(cls):
        for section, srv in cls._ocean._all_services():
            srvd = cls._ocean._get(srv)
            if "cron" in srvd and "monthly" in srvd["cron"]:
                cmd = srvd["cron"]["monthly"]
                cls._ocean.shell(srv, "-c", cmd)
