import unittest

from mock import Mock, patch

from tcell_agent.appsensor.injections_reporter import InjectionsReporter
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.params import GET_PARAM, POST_PARAM, JSON_PARAM, COOKIE_PARAM, URI_PARAM
from tcell_agent.appsensor.sensors.injection_sensor import InjectionAttempt

# set is builtin in python 3 but a module in earlier version
try:
    set
except NameError:
    from sets import Set as set


class InjectionsReporterTest(unittest.TestCase):
    def no_matches_check_test(self):
        payloads_policy = Mock()
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = (_ for _ in ())
        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, False)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        injections_reporter.check(appsensor_meta)

    def one_get_injection_match_check_full_uri_test(self):
        self.one_get_injection_match_check(True)

    def one_get_injection_match_check_test(self):
        self.one_get_injection_match_check(False)

    def one_get_injection_match_check(self, collect_full_uri):
        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = iter([
            InjectionAttempt(GET_PARAM, "xss", {"param": "dirty", "value": "<script>", "pattern": "1"})
        ])

        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, collect_full_uri)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        with patch('tcell_agent.appsensor.injections_reporter.send_event') as patched_send_event:
            injections_reporter.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="xss",
                parameter="dirty",
                meta={"l": "query"},
                payload=None,
                pattern="1",
                collect_full_uri=collect_full_uri)

    def one_post_injection_match_check_test(self):
        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = iter([
            InjectionAttempt(POST_PARAM, "xss", {"param": "dirty", "value": "<script>", "pattern": "1"})
        ])

        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, False)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        with patch('tcell_agent.appsensor.injections_reporter.send_event') as patched_send_event:
            injections_reporter.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="xss",
                parameter="dirty",
                meta={"l": "body"},
                payload=None,
                pattern="1",
                collect_full_uri=False)

    def one_json_injection_match_check_test(self):
        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = iter([
            InjectionAttempt(JSON_PARAM, "xss", {"param": "dirty", "value": "<script>", "pattern": "1"})
        ])

        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, False)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        with patch('tcell_agent.appsensor.injections_reporter.send_event') as patched_send_event:
            injections_reporter.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="xss",
                parameter="dirty",
                meta={"l": "body"},
                payload=None,
                pattern="1",
                collect_full_uri=False)

    def one_uri_injection_match_check_test(self):
        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = iter([
            InjectionAttempt(URI_PARAM, "xss", {"param": "dirty", "value": "<script>", "pattern": "1"})
        ])

        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, False)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        with patch('tcell_agent.appsensor.injections_reporter.send_event') as patched_send_event:
            injections_reporter.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="xss",
                parameter="dirty",
                meta={"l": "uri"},
                payload=None,
                pattern="1",
                collect_full_uri=False)

    def one_cookie_injection_match_check_test(self):
        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        injections_matcher = Mock()
        injections_matcher.each_injection.return_value = iter([
            InjectionAttempt(COOKIE_PARAM, "xss", {"param": "dirty", "value": "<script>", "pattern": "1"})
        ])

        injections_reporter = InjectionsReporter(injections_matcher, payloads_policy, False)

        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"

        with patch('tcell_agent.appsensor.injections_reporter.send_event') as patched_send_event:
            injections_reporter.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="xss",
                parameter="dirty",
                meta={"l": "cookie"},
                payload=None,
                pattern="1",
                collect_full_uri=False)
