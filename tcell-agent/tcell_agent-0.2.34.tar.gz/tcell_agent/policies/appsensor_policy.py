# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from future.utils import iteritems
from tcell_agent.appsensor.injections_reporter import InjectionsReporter
from tcell_agent.instrumentation import safe_wrap_function
from tcell_agent.policies import TCellPolicy
from tcell_agent.appsensor.sensors import CmdiSensor
from tcell_agent.appsensor.sensors import DatabaseSensor
from tcell_agent.appsensor.sensors import FptSensor
from tcell_agent.appsensor.sensors import MiscSensor
from tcell_agent.appsensor.sensors import NullbyteSensor
from tcell_agent.appsensor.sensors import RequestSizeSensor
from tcell_agent.appsensor.sensors import ResponseCodesSensor
from tcell_agent.appsensor.sensors import ResponseSizeSensor
from tcell_agent.appsensor.sensors import RetrSensor
from tcell_agent.appsensor.sensors import SqliSensor
from tcell_agent.appsensor.sensors import UserAgentSensor
from tcell_agent.appsensor.sensors import XssSensor
from tcell_agent.appsensor.sensors import PayloadsPolicy


class AppSensorPolicy(TCellPolicy):
    api_identifier = "appsensor"

    options_v2_classes = {
        "req_size": RequestSizeSensor,
        "resp_size": ResponseSizeSensor,
        "resp_codes": ResponseCodesSensor,
        "xss": XssSensor,
        "sqli": SqliSensor,
        "cmdi": CmdiSensor,
        "fpt": FptSensor,
        "nullbyte": NullbyteSensor,
        "retr": RetrSensor,
        "ua": UserAgentSensor,
        "errors": MiscSensor,
        "database": DatabaseSensor}

    DETECTION_POINTS_V2_NON_INJECTION = {
        "req_size": RequestSizeSensor,
        "resp_size": ResponseSizeSensor,
        "resp_codes": ResponseCodesSensor,
        "ua": UserAgentSensor,
        "errors": MiscSensor,
        "database": DatabaseSensor
    }

    def __init__(self, policy_json=None):
        super(AppSensorPolicy, self).__init__()
        self.init_variables()
        if policy_json is not None:
            self.loadFromJson(policy_json)

    def init_variables(self):
        self.enabled = False
        self.options = {}
        self.injections_reporter = InjectionsReporter.from_json(
            version=0,
            data_json={},
            payloads_policy=PayloadsPolicy(),
            collect_full_uri=False)

    def process_appsensor_meta(self, appsensor_meta):
        if not self.enabled:
            return

        self.check_request_size(appsensor_meta)
        self.check_response_size(appsensor_meta)
        self.check_response_code(appsensor_meta)

        self.injections_reporter.check(appsensor_meta)

        if "ua" in self.options:
            safe_wrap_function(
                "Check User Agent",
                self.options["ua"].check,
                appsensor_meta
            )

    def should_check_db_rows(self, route_id):
        return "database" in self.options and self.options["database"].should_check(route_id)

    def check_db_rows(self, appsensor_meta, number_of_records):
        if "database" in self.options:
            safe_wrap_function(
                "Appsensor Check Number of DB Rows",
                self.options["database"].check,
                appsensor_meta,
                number_of_records
            )

    def check_request_size(self, appsensor_meta):
        if "req_size" in self.options:
            safe_wrap_function(
                "Check Request Size",
                self.options["req_size"].check,
                appsensor_meta)

    def check_response_size(self, appsensor_meta):
        if "resp_size" in self.options:
            safe_wrap_function(
                "Check Response Size",
                self.options["resp_size"].check,
                appsensor_meta)

    def check_response_code(self, appsensor_meta):
        if "resp_codes" in self.options:
            safe_wrap_function(
                "Check Response Codes",
                self.options["resp_codes"].check,
                appsensor_meta,
                appsensor_meta.response_code)

    def csrf_rejected(self, appsensor_meta):
        if "errors" in self.options:
            safe_wrap_function(
                "CSRF Exception processing",
                self.options["errors"].csrf_rejected,
                appsensor_meta)

    def sql_exception_detected(self, appsensor_meta, exc_type_name, traceback):
        if "errors" in self.options:
            safe_wrap_function(
                "SQL Exception processing",
                self.options["errors"].sql_exception_detected,
                appsensor_meta,
                exc_type_name,
                traceback)

    def loadFromJson(self, policy_json):
        if "policy_id" in policy_json:
            self.policy_id = policy_json["policy_id"]
        else:
            raise Exception("Policy Id Not Found")

        self.init_variables()

        policy_data = policy_json.get("data")

        if "version" in policy_json and policy_json["version"] == 2:
            if policy_data:
                sensors_json = policy_data.get("sensors")

                if not sensors_json:
                    self.enabled = False

                elif sensors_json:
                    self.enabled = True

                    options = policy_data.get("options", {})
                    payloads_policy = PayloadsPolicy.from_json(options)
                    collect_full_uri = options.get("uri_options", {}).get("collect_full_uri", False)

                    self.injections_reporter = InjectionsReporter.from_json(
                        version=2,
                        data_json=sensors_json,
                        payloads_policy=payloads_policy,
                        collect_full_uri=collect_full_uri)

                    for option, clazz in iteritems(self.DETECTION_POINTS_V2_NON_INJECTION):
                        updated_settings = {"enabled": option in sensors_json,
                                            "collect_full_uri": collect_full_uri}
                        updated_settings.update(sensors_json.get(option, {}))
                        self.options[option] = clazz(updated_settings)

        else:
            if policy_data:
                options_json = policy_data.get("options")

                if not options_json:
                    self.enabled = False

                elif options_json:
                    self.enabled = True

                    payloads_policy = PayloadsPolicy.from_json({
                        "payloads": {
                            "send_payloads": True,
                            "log_payloads": True
                        }
                    })

                    self.injections_reporter = InjectionsReporter.from_json(
                        version=1,
                        data_json=policy_data,
                        payloads_policy=payloads_policy,
                        collect_full_uri=False)

                    enabled = options_json.get("req_res_size", False)
                    self.options["req_size"] = RequestSizeSensor({"enabled": enabled})
                    self.options["resp_size"] = ResponseSizeSensor({"enabled": enabled})

                    enabled = options_json.get("resp_codes", False)
                    self.options["resp_codes"] = ResponseCodesSensor({
                        "enabled": enabled,
                        "series_400_enabled": True,
                        "series_500_enabled": True})

                    self.options["ua"] = UserAgentSensor({"enabled": False, "empty_enabled": False})
                    self.options["errors"] = MiscSensor(
                        {"csrf_exception_enabled": False, "sql_exception_enabled": False})
                    self.options["database"] = DatabaseSensor({"enabled": False})
