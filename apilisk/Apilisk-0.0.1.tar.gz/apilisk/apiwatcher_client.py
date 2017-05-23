"""
Client for apiwatcher platform
"""
from requests.exceptions import ConnectionError

from apiwatcher_pyclient.client import Client
from apilisk.printer import vprint, Colors
from apilisk.exceptions import ObjectNotFound, ApiliskException

class ApiwatcherClient:
    """
    Client using apiwatcher-pyclient to communicate with the platform
    """

    def __init__(self, apilisk_cfg):
        """
        Initialize and log in to platform
        """
        try:
            self.client = Client(
                apilisk_cfg["host"], apilisk_cfg["port"], verify_certificate=False
                )

            vprint(
                1, Colors.GREEN,
                "### Authorizing to {0}".format(apilisk_cfg["host"])
            )

            self.client.authorize_client_credentials(
                apilisk_cfg["client_id"], apilisk_cfg["client_secret"],
                "private_agent"
            )
            vprint(1, Colors.GREEN, "### Authorization done")
        except ConnectionError as e:
            raise ApiliskException(
                "Could not connect to Apiwatcher platform: {0}".format(
                    e.message
                )
            )


    def get_project_config(self, project_hash):
        """
        Return configuration of a project
        """

        vprint(
            1, Colors.GREEN,
            "### Getting configuraton of project {0}".format(project_hash)
        )

        rsp = self.client.get(
            "/api/projects/{0}/configuration".format(project_hash)
        )
        if rsp.status_code == 404:
            raise ObjectNotFound(
                "Project with hash {0} has not been found".format(
                    project_hash
                )
            )
        elif rsp.status_code != 200:
            raise ApiliskException(
                "Could not get configuration of project {0}: {1}".format(
                    project_hash, rsp.json()["message"]
                )
            )

        vprint(1, Colors.GREEN,"### Configuration downloaded")
        cfg = rsp.json()["data"]
        vprint(
            2, Colors.GREEN,
            "### Summary: {0} testcases, {1} requests, {2} datasets".format(
                len(cfg["testcases"]), len(cfg["requests"]),
                len(cfg["datasets"])
            ))

        return cfg


        return rsp.json()["data"]
