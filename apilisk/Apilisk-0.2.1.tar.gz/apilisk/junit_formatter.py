# -*- coding: utf-8 -*-

import json
from junit_xml import TestSuite, TestCase


class JunitFormatter(object):

    def __init__(self, project_cfg, project_result):
        """Initialize the stuff"""
        self.testcases = {
            unicode(item["id"]): item for item in project_cfg["testcases"]
        }

        test_cases = []
        for case in project_result["results"]:
            tc = TestCase(
                u"{0}".format(self.testcases[str(case["testcase_id"])]["name"]),
                elapsed_sec=case["duration_sec"]
            )
            if case["status"] == "failed":
                # Last error and first error message
                tc.add_error_info(case["steps_results"][-1]["errors"][0]["message"])

            test_cases.append(tc)

        self.test_suite = TestSuite(
            name=u"Project {0}".format(project_cfg["project_name"]),
            test_cases=test_cases
        )

    def to_file(self, filename):
        """
        Output project results to specified filename
        """
        with open(filename, 'w') as f:
            f.write(
                TestSuite.to_xml_string(
                    [self.test_suite], prettyprint=True, encoding="utf-8"
                ).encode("utf-8")
            )
