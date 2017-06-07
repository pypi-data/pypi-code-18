from dotmap import DotMap
from requests.exceptions import ConnectionError

from unittest import TestCase
from unittest.mock import patch, call

from rancon.backends import consul
from .test_data import TEST_SERVICES


class TestConsulStatic(TestCase):

    def setUp(self):
        self.consul = consul.ConsulBackend(url="http://loglhost:7500")

    @patch('rancon.backends.consul.consul')
    def test_register(self, mock):
        con = self.consul.register(TEST_SERVICES[0])
        consul_mock = mock.Consul
        self.assertTrue(consul_mock.called)
        consul_mock.assert_called_with(host="loglhost", port=7500, scheme='http')


class TestConsulDynamic(TestCase):

    def setUp(self):
        self.consul = consul.ConsulBackend(url="http://%HOST%")

    @patch('rancon.backends.consul.consul')
    def test_register(self, mock):
        def register_mock(*args, **kwargs):
            return args[1]
        # prepare side effect
        consul_mock = mock.Consul
        mock_agent = consul_mock.return_value.agent.service.register
        mock_agent.side_effect = register_mock
        _, con0 = self.consul.register(TEST_SERVICES[0])
        self.assertEqual(1, len(self.consul.consul_inst_cache))
        _, con1 = self.consul.register(TEST_SERVICES[1])
        self.assertEqual(2, len(self.consul.consul_inst_cache))
        # check return values
        self.assertEqual('1-host-1-101', con0)
        self.assertEqual('2-host-2-102', con1)
        # check calls
        self.assertTrue(consul_mock.called)
        # nice:
        # http://stackoverflow.com/questions/7242433/asserting-successive-calls-to-a-mock-method
        consul_mock.assert_any_call(host="host_1", port=8500, scheme='http')
        consul_mock.assert_any_call(host="host_2", port=8500, scheme='http')
        self.assertEqual(2, consul_mock.call_count)
        self.assertTrue(mock_agent.called)
        taglist = ['rancon-default']
        mock_agent.assert_has_calls((
            call('1', '1-host-1-101', address='host_1', port=101, tags=taglist),
            call('2', '2-host-2-102', address='host_2', port=102, tags=taglist)
        ))

    @patch('rancon.backends.consul.consul')
    def test_register_caught_exception(self, mock):
        # prepare side effect
        consul_mock = mock.Consul
        mock_agent = consul_mock.return_value.agent.service.register
        mock_agent.side_effect = [ConnectionError('Exception Test'),
                                  TEST_SERVICES[1]]
        succ0, con0 = self.consul.register(TEST_SERVICES[0])
        succ1, con1 = self.consul.register(TEST_SERVICES[1])
        self.assertFalse(succ0)
        self.assertTrue(succ1)
        # all other behavior is checked in the "working" test
