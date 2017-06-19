"""
Client for apiwatcher platform
"""
from requests.exceptions import ConnectionError

from apiwatcher_pyclient.client import Client
from apiwatcher_pyclient.exceptions import ApiwatcherClientException
from apilisk.printer import vprint, Colors, eprint
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
            self.agent_id = apilisk_cfg["agent_id"]
            self.client = Client(
                apilisk_cfg["host"], apilisk_cfg["port"],
                verify_certificate=True
            )

            vprint(
                1, None,
                "### Authorizing to {0} ... ".format(apilisk_cfg["host"]), True
            )

            self.client.authorize_client_credentials(
                apilisk_cfg["client_id"], apilisk_cfg["client_secret"],
                "private_agent"
            )
            vprint(
                1, Colors.GREEN,
                "\r### Authorizing to {0} ... OK".format(apilisk_cfg["host"])
            )

        except KeyError as e:
            raise ApiliskException(
                "Key {0} is missing in configuration file.".format(e.message)
            )
        except ApiwatcherClientException as e:
            raise ApiliskException(
                "Could not authenticate to Apiwatcher platform: {0}".format(
                    e.message
                )
            )
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
            1, None,
            "### Getting configuraton of project {0} ... ".format(project_hash),
            True
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

        vprint(
            1, Colors.GREEN,
            "\r### Getting configuraton of project {0} ... OK".format(project_hash)
        )
        cfg = rsp.json()["data"]
        vprint(
            2, Colors.GREEN,
            "### Summary: {0} testcases, {1} requests, {2} datasets".format(
                len(cfg["testcases"]), len(cfg["requests"]),
                len(cfg["datasets"])
            ))

        return cfg

    def upload_results(self, config, results):
        """Upload data to platform"""
        vprint(
            1, None,
            "### Uploading data to Apiwatcher platform ...", True
        )

        rsp = self.client.post(
            "/api/projects/{0}/remote-results".format(results["project_hash"]),
            data={
                "agent_id": self.agent_id,
                "configuration": config,
                "results": results
            }
        )

        if rsp.status_code == 201:
            vprint(
                1, Colors.GREEN,
                "\r### Uploading data to Apiwatcher platform ... OK"
            )
        else:
            eprint("### Upload failed with response code {0}".format(rsp.status_code))
