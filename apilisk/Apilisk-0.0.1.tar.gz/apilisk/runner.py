import json
import copy

from datetime import datetime

from apilisk.curl_caller import CurlCaller
from apilisk.printer import vprint, Colors
from apilisk.exceptions import ObjectNotFound, ApiliskException
from apiwatcher_pyclient.client import Client


class Runner(object):

    def __init__(self, project_cfg, dataset_id):
        """
        Initializes all the stuff
        """
        self.project_hash = project_cfg["project_hash"]
        self.testcases = {
            str(item["id"]): item for item in project_cfg["testcases"]
        }
        self.requests = {
            str(item["id"]): item for item in project_cfg["requests"]
        }

        self.dataset = None
        if dataset_id is not None:
            for dts in project_cfg["datasets"]:
                if dts["id"] == dataset_id:
                 self.dataset = copy.deepcopy(dts)

            if self.dataset == None:
                raise ObjectNotFound(
                    "Dataset with id {0} has not been found".format(
                        dataset_id
                    )
                )

    def run_project(self, debug=False):
        """
        Runs testcases from project one project
        """
        results = []
        for tc_id in self.testcases:
            results.append(self.run_one_testcase(tc_id, debug))

        return {
            "project_hash": self.project_hash,
            "results": results
        }

    def run_one_testcase(self, tc_id, debug=False):
        """
        Runs a single testcase
        """
        # Merge dataset variables and request variables
        variables = {
            "var": copy.deepcopy(
                self.dataset["variables"]
            ) if self.dataset is not None else {},
            "req": []
        }

        auth = self.testcases[tc_id]["authentication"]
        status = "success"
        results = []

        time_start = datetime.now()

        for step in self.testcases[tc_id]["steps"]:
            if step["action"] == "call_request":
                caller = CurlCaller(
                    step["data"], variables, authentication=auth, debug=debug
                )
                result, req_var = caller.handle_and_get_report()
                variables["req"].append(req_var)

                results.append(result)

                if result["status"] == "failed":
                    status = "failed"
                    break

        return {
            "testcase_id": tc_id,
            "results": results,
            "status": status,
            "duration_sec": (datetime.now() - time_start).total_seconds()
        }
