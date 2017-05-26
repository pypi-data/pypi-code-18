import traceback

from tcell_agent.appsensor.sensor import send_event


class MiscSensor(object):
    def __init__(self, policy_json=None):
        self.csrf_exception_enabled = False
        self.sql_exception_enabled = False
        self.excluded_route_ids = {}
        self.collect_full_uri = False

        if policy_json is not None:
            self.csrf_exception_enabled = policy_json.get("csrf_exception_enabled", False)
            self.sql_exception_enabled = policy_json.get("sql_exception_enabled", False)
            self.collect_full_uri = policy_json.get("collect_full_uri", self.collect_full_uri)

            for route_id in policy_json.get("exclude_routes", []):
                self.excluded_route_ids[route_id] = True

    def csrf_rejected(self, appsensor_meta):
        if not self.csrf_exception_enabled:
            return

        if self.excluded_route_ids.get(appsensor_meta.route_id, False):
            return False

        send_event(
            appsensor_meta=appsensor_meta,
            detection_point="excsrf",
            parameter=None,
            meta=None,
            collect_full_uri=self.collect_full_uri)

    def sql_exception_detected(self, appsensor_meta, exc_type_name, tb):
        if not self.sql_exception_enabled:
            return

        if self.excluded_route_ids.get(appsensor_meta.route_id, False):
            return False

        stack_trace = traceback.format_tb(tb)
        stack_trace.reverse()

        send_event(
            appsensor_meta=appsensor_meta,
            detection_point="exsql",
            parameter=exc_type_name,
            meta=None,
            payload=''.join(stack_trace),
            collect_full_uri=self.collect_full_uri)

    def __str__(self):
        return "<%s csrf_exception_enabled: %s sql_exception_enabled: %s>" % \
               (type(self).__name__, self.csrf_exception_enabled, self.sql_exception_enabled)
