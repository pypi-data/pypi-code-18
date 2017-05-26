import unittest

from mock import patch

from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.sensors import MiscSensor


class MiscSensorTest(unittest.TestCase):
    def create_default_sensor_test(self):
        sensor = MiscSensor()
        self.assertFalse(sensor.csrf_exception_enabled)
        self.assertFalse(sensor.sql_exception_enabled)

    def create_enabled_sensor_test(self):
        sensor = MiscSensor({
            'csrf_exception_enabled': True,
            'sql_exception_enabled': True
        })
        self.assertTrue(sensor.csrf_exception_enabled)
        self.assertTrue(sensor.sql_exception_enabled)

    def with_disabled_sensor_csrf_rejected_test(self):
        sensor = MiscSensor({'csrf_exception_enabled': False})
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = 'remote_addr'
        appsensor_meta.method = 'request_method'
        appsensor_meta.location = 'abosolute_uri'
        appsensor_meta.route_id = '23947'
        appsensor_meta.session_id = 'session_id'
        appsensor_meta.user_id = 'user_id'

        with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
            sensor.csrf_rejected(appsensor_meta)
            self.assertFalse(patched_send_event.called)

    def with_enabled_sensor_csrf_rejected_test(self):
        sensor = MiscSensor({'csrf_exception_enabled': True})
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = 'remote_addr'
        appsensor_meta.method = 'request_method'
        appsensor_meta.location = 'abosolute_uri'
        appsensor_meta.route_id = '23947'
        appsensor_meta.session_id = 'session_id'
        appsensor_meta.user_id = 'user_id'

        with patch('tcell_agent.appsensor.sensors.misc_sensor.send_event') as patched_send_event:
            sensor.csrf_rejected(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point="excsrf",
                parameter=None,
                meta=None,
                collect_full_uri=False)
