from tcell_agent.appsensor.sensor import send_event


class UserAgentSensor(object):
    DP_CODE = "uaempty"

    def __init__(self, policy_json=None):
        self.enabled = False
        self.empty_enabled = False
        self.excluded_route_ids = {}
        self.collect_full_uri = False

        if policy_json is not None:
            self.enabled = policy_json.get("enabled", False)
            self.empty_enabled = policy_json.get("empty_enabled", False)
            self.collect_full_uri = policy_json.get("collect_full_uri", self.collect_full_uri)

            for route_id in policy_json.get("exclude_routes", []):
                self.excluded_route_ids[route_id] = True

    def check(self, appsensor_meta):
        if not self.enabled or not self.empty_enabled:
            return

        if self.excluded_route_ids.get(appsensor_meta.route_id, False):
            return False

        if not (appsensor_meta.user_agent_str and appsensor_meta.user_agent_str.strip()):
            send_event(
                appsensor_meta=appsensor_meta,
                detection_point=self.DP_CODE,
                parameter=None,
                meta=None,
                collect_full_uri=self.collect_full_uri)

    def __str__(self):
        return "<%s enabled: %s empty_enabled: %s dp_code: %s>" % \
               (type(self).__name__, self.enabled, self.empty_enabled, self.DP_CODE)
