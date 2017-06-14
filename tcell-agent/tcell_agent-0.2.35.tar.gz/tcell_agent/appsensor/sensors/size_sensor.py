from tcell_agent.appsensor.sensor import send_event


def convert_to_kibibytes(bytes_len):
    return bytes_len / float(1024)


class SizeSensor(object):
    MAX_NORMAL_REQUEST_BYTES = 1024 * 512
    DP_UNUSUAL_REQUEST_SIZE = "reqsz"

    def __init__(self, default_limit, dp_code, policy_json=None):
        self.enabled = False
        self.limit = default_limit
        self.dp_code = dp_code
        self.excluded_route_ids = {}
        self.collect_full_uri = False

        if policy_json is not None:
            self.enabled = policy_json.get("enabled", False)
            self.limit = policy_json.get("limit", self.limit)
            self.collect_full_uri = policy_json.get("collect_full_uri", self.collect_full_uri)

            for route_id in policy_json.get("exclude_routes", []):
                self.excluded_route_ids[route_id] = True

    def get_size(self, appsensor_meta):
        raise NotImplementedError()

    def check(self, appsensor_meta):
        if not self.enabled or self.excluded_route_ids.get(appsensor_meta.route_id, False):
            return

        content_size = self.get_size(appsensor_meta)
        size_KiB = convert_to_kibibytes(content_size)
        if size_KiB > self.limit:
            send_event(
                appsensor_meta=appsensor_meta,
                detection_point=self.dp_code,
                parameter=None,
                meta={"sz": content_size},
                collect_full_uri=self.collect_full_uri)

    def __str__(self):
        return "<%s enabled: %s limit: %s dp_code: %s excluded_route_ids: %s>" % \
               (type(self).__name__, self.enabled, self.limit, self.dp_code, self.excluded_route_ids)
