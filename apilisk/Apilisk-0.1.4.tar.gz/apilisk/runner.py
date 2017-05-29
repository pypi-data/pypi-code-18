import json
import copy
import pytz
import sys

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
        self.project_name = project_cfg["project_name"]
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
                    u"Dataset with id {0} has not been found".format(
                        dataset_id
                    )
                )

    def run_project(self, debug=False, include_data=False):
        """
        Runs testcases from project one project
        """
        results = []

        time_start = datetime.now()

        total_count = len(self.testcases)
        success_count = 0
        failed_count = 0
        vprint(
            1, None,
            u"## Starting project {0} ({1})".format(
                self.project_name, self.project_hash
            )
        )
        for tc_id in self.testcases:
            res = self.run_one_testcase(tc_id, debug, include_data)
            if res["status"] == "success":
                success_count += 1
            else:
                failed_count += 1
            results.append(res)

        duration_sec = (datetime.now() - time_start).total_seconds()

        if failed_count > 0:
            vprint(
                1, Colors.RED,
                u"## Failed {0} testcases out of {1} in {2} sec.".format(
                    failed_count, total_count, duration_sec
                )
            )
        else:
            vprint(
                1, Colors.GREEN, u"## Success in {0} sec".format(duration_sec)
            )

        return {
            "project_hash": self.project_hash,
            "total_count": total_count,
            "success_count": success_count,
            "failed_count": failed_count,
            "duration_sec": duration_sec,
            "results": results
        }

    def run_one_testcase(self, tc_id, debug=False, include_data=False):
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

        vprint(
            1, None, u"# {0} ... ".format(
                self.testcases[tc_id]["name"]
            ), True
        )

        for step in self.testcases[tc_id]["steps"]:
            if step["action"] == "call_request":
                caller = CurlCaller(
                    step["data"], variables, authentication=auth, debug=debug
                )
                result, req_var = caller.handle_and_get_report(
                    include_data=include_data
                )
                variables["req"].append(req_var)
                results.append(result)

                if result["status"] == "failed":
                    status = "failed"
                    break


        if status == 'success':
            vprint(
                1, Colors.GREEN, u"\r# {0} ... SUCCESS".format(
                    self.testcases[tc_id]["name"]
                )
            )
        else:
            vprint(
                1, Colors.RED, u"\r# {0} ... FAILED".format(
                    self.testcases[tc_id]["name"]
                )
            )

        return {
            "testcase_id": int(tc_id),
            "steps_results": results,
            "status": status,
            "duration_sec": (datetime.now() - time_start).total_seconds()
        }
