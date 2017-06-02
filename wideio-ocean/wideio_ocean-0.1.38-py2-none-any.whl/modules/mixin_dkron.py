import hashlib

import requests

# used by nginx, passwordreminders, static websites reconstruction (equity, kashflow, propsearch...)

SCHED_MAP = {
    "hourly": "1 1 * * * *",
    "daily": "2 2 2 * *",
    "weekly": "3 3 3 * * 3",
    "monthly": "4 4 4 4 * *"
}


class MixIn(object):
    """
    Manages a system distributed dkrontab for the specified manifest file.
    """

    @classmethod
    def dkron_register(cls):
        """Register for events in the dkron daemon."""
        dkron_h = cls._dkron_h()
        URL = cls._ocean._get_config("dkron.url", "http://localhost:8080/")
        for p in ["hourly", "daily", "weekly", "monthly"]:
            cmd = (("/bin/bash -c 'OCEANPATH=%s\nexport OCEAN_MANIFEST=%s\nocean dkron_run_" + p + "'")
                   % (cls._ocean.OCEANPATH, cls._ocean.OCEAN_MANIFEST))
            requests.post(URL + "v1/jobs", {"name": "ocean-" + dkron_h + "-" + p,
                                            "schedule": SCHED_MAP[p],
                                            "command": cmd
                                            })

    @classmethod
    def _dkron_h(cls):
        dkron_h = "%s" % (hashlib.md5(cls._ocean.MP.encode('utf8')).hexdigest()[:16:2],)
        return dkron_h

    @classmethod
    def dkron_run_hourly(cls):
        """Called by dkron to run all tasks that shal be run hourly."""

        for section, srv in cls._ocean._all_services():
            srvd = cls._get(srv)
            if "dkron" in srvd and "hourly" in srvd["dkron"]:
                cmd = srvd["dkron"]["hourly"]
                cls.shell(srv, "-c", cmd)

    @classmethod
    def dkron_run_daily(cls):
        """Called by dkron to run all tasks that shal be run daily."""

        for section, srv in cls._ocean._all_services():
            srvd = cls._get(srv)
            if "dkron" in srvd and "daily" in srvd["dkron"]:
                cmd = srvd["dkron"]["daily"]
                cls.shell(srv, "-c", cmd)

    @classmethod
    def dkron_run_weekly(cls):
        """Called by dkron to run all tasks that shal be run weekly."""

        for section, srv in cls._ocean._all_services():
            srvd = cls._get(srv)
            if "dkron" in srvd and "weekly" in srvd["dkron"]:
                cmd = srvd["dkron"]["weekly"]
                cls.shell(srv, "-c", cmd)

    @classmethod
    def dkron_run_monthly(cls):
        """Called by dkron to run all tasks that shal be run monthly."""

        for section, srv in cls._ocean._all_services():
            srvd = cls._get(srv)
            if "dkron" in srvd and "monthly" in srvd["ckron"]:
                cmd = srvd["dkron"]["monthly"]
                cls.shell(srv, "-c", cmd)
