from unittest import TestCase
from unittest.mock import patch, call

import rancon
from rancon.backends import consul
from .test_data import TEST_SERVICES


class TestMainLoop(TestCase):

    def setUp(self):
        self.consul = consul.ConsulBackend(url="http://%HOST%")
        rancon.settings.loglevel = 0

    @patch('rancon.settings.source')
    @patch('rancon.backends.consul.consul')
    def test_register_uncaught_exception(self, consul_mock, settings_mock):
        # prepare side effect
        rancon.settings.backend = self.consul
        consul_mock = consul_mock.Consul

        # we have two services
        settings_mock.get_services.side_effect = [TEST_SERVICES[0:2]]

        # of which the first registration throws an exception
        mock_agent = consul_mock.return_value.agent.service.register
        mock_agent.side_effect = [ConnectionError('Exception Test'),
                                  TEST_SERVICES[1]]

        # now go.
        rancon.route_services()

        # basically copied from other test. unfortunately creating a common
        # validation method proved too annoying.
        consul_mock.assert_any_call(host="host_1", port=8500, scheme='http')
        consul_mock.assert_any_call(host="host_2", port=8500, scheme='http')
        self.assertEqual(2, consul_mock.call_count)
        self.assertTrue(mock_agent.called)
        taglist = ['rancon-default']
        mock_agent.assert_has_calls((
            call('1', '1-host-1-101', address='host_1', port=101, tags=taglist),
            call('2', '2-host-2-102', address='host_2', port=102, tags=taglist)
        ))
