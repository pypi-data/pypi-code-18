from tcell_agent.instrumentation.django.utils import django15or16
if not django15or16:
    import unittest

    from mock import patch, Mock

    from django.db.utils import ProgrammingError, OperationalError

    from tcell_agent.appsensor.meta import AppSensorMeta  # pylint: disable=ungrouped-imports
    from tcell_agent.appsensor.sensors import MiscSensor

    class MiscSensorSqlExceptionTest(unittest.TestCase):

        def with_disabled_sensor_sql_exception_test(self):
            sensor = MiscSensor({"sql_exception_enabled": False})

            with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
                with patch('traceback.format_tb', return_value=['stack', 'trace']) as patched_format_tb:
                    meta = Mock()
                    exc_type = ProgrammingError
                    tb = Mock()

                    sensor.sql_exception_detected(meta, exc_type.__name__, tb)
                    self.assertFalse(patched_send_event.called)
                    self.assertFalse(patched_format_tb.called)

        def with_enabled_sensor_sql_exception_test(self):
            sensor = MiscSensor({'sql_exception_enabled': True})
            appsensor_meta = AppSensorMeta()
            appsensor_meta.remote_address = 'remote_addr'
            appsensor_meta.method = 'request_method'
            appsensor_meta.location = 'abosolute_uri'
            appsensor_meta.route_id = '23947'
            appsensor_meta.session_id = 'session_id'
            appsensor_meta.user_id = 'user_id'

            with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
                with patch('traceback.format_tb', return_value=['stack', 'trace']) as patched_format_tb:
                    exc_type = ProgrammingError
                    tb = Mock()

                    sensor.sql_exception_detected(appsensor_meta, exc_type.__name__, tb)
                    patched_send_event.assert_called_once_with(
                        appsensor_meta=appsensor_meta,
                        detection_point="exsql",
                        parameter="ProgrammingError",
                        meta=None,
                        payload='tracestack',
                        collect_full_uri=False)
                    patched_format_tb.assert_called_once_with(tb)

        def with_enabled_sensor_sql_exception_operational_error_test(self):
            sensor = MiscSensor({'sql_exception_enabled': True})
            appsensor_meta = AppSensorMeta()
            appsensor_meta.remote_address = 'remote_addr'
            appsensor_meta.method = 'request_method'
            appsensor_meta.location = 'abosolute_uri'
            appsensor_meta.route_id = '23947'
            appsensor_meta.session_id = 'session_id'
            appsensor_meta.user_id = 'user_id'

            with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
                with patch('traceback.format_tb', return_value=['stack', 'trace']) as patched_format_tb:
                    exc_type = OperationalError
                    tb = Mock()

                    sensor.sql_exception_detected(appsensor_meta, exc_type.__name__, tb)
                    patched_send_event.assert_called_once_with(
                        appsensor_meta=appsensor_meta,
                        detection_point='exsql',
                        parameter='OperationalError',
                        meta=None,
                        payload='tracestack',
                        collect_full_uri=False)
                    patched_format_tb.assert_called_once_with(tb)

        def with_enabled_sensor_sql_exception_matching_excluded_route_test(self):
            sensor = MiscSensor({'sql_exception_enabled': True, 'exclude_routes': ['23947']})
            appsensor_meta = AppSensorMeta()
            appsensor_meta.remote_address = 'remote_addr'
            appsensor_meta.method = 'request_method'
            appsensor_meta.location = 'abosolute_uri'
            appsensor_meta.route_id = '23947'
            appsensor_meta.session_id = 'session_id'
            appsensor_meta.user_id = 'user_id'

            with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
                with patch('traceback.format_tb', return_value=['stack', 'trace']) as patched_format_tb:
                    exc_type = ProgrammingError
                    tb = Mock()

                    sensor.sql_exception_detected(appsensor_meta, exc_type.__name__, tb)
                    self.assertFalse(patched_send_event.called)
                    self.assertFalse(patched_format_tb.called)

        def with_enabled_sensor_sql_exception_nonmatching_excluded_route_test(self):
            sensor = MiscSensor({'sql_exception_enabled': True, 'exclude_routes': ['nonmatching']})
            appsensor_meta = AppSensorMeta()
            appsensor_meta.remote_address = 'remote_addr'
            appsensor_meta.method = 'request_method'
            appsensor_meta.location = 'abosolute_uri'
            appsensor_meta.route_id = '23947'
            appsensor_meta.session_id = 'session_id'
            appsensor_meta.user_id = 'user_id'

            with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
                with patch('traceback.format_tb', return_value=['stack', 'trace']) as patched_format_tb:
                    exc_type = ProgrammingError
                    tb = Mock()

                    sensor.sql_exception_detected(appsensor_meta, exc_type.__name__, tb)
                    patched_send_event.assert_called_once_with(
                        appsensor_meta=appsensor_meta,
                        detection_point="exsql",
                        parameter="ProgrammingError",
                        meta=None,
                        payload='tracestack',
                        collect_full_uri=False)
                    patched_format_tb.assert_called_once_with(tb)
