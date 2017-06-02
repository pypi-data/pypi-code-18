# - look if new artifcact is available from server or git and reconstruct the images
# - and auto-re-deploy the system with latest changes pushed in prod
import json

import requests
from requests.auth import HTTPBasicAuth


class MixIn(object):
    """
    Set of commands to perform the following:

    Attempts to download latest version of images present in the manifest from the docker-registry and
    reload the images as necessary.

    Ideally, these commands are put in a CRON with some escalation rules.
    """

    @classmethod
    def autoupdate_check_docker_registry_updates(cls):
        """
        Return a list of updated servers and an updated manifest.
        """
        steps = [x[1] for x in cls._ocean._PIPELINE]
        assert steps
        # for all services
        #    if _prev_step.ts > _next_step.ts
        if False:
            kwargs = {}

            if kwargs:
                kwargs["auth"] = HTTPBasicAuth(*requests._get_config("autoupdate_repo.auth"))
                # ^ FIXME: Auth should be read from docker-config.json

            res = json.loads(requests.get("/v2/%s/manifests/%s", **kwargs))
            assert res

    @classmethod
    def autoupdate_rebuild(cls):
        """
        Based on GIT updates - try to autorebuild the image that needs rebuilding.
        """
        # rebuild if rebuild is enabled or reload image from cache if rebuild is disabled
        pass

    @classmethod
    def autoupdate_reload(cls):
        # rebuild if rebuild is enabled or reload image from cache if rebuild is disabled
        """
        After an update - try to auto reload the service that need to be reloaded.
        """
        pass
