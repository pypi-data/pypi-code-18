import ast
import unittest

import pytest

from pubsub.adapters import GoogleCloudAdapter


class TestAdapters(unittest.TestCase):

    # Kafka needs work before it can be added.
    # adapters_list = [GoogleCloudAdapter()]

    def setUp(self):
        self.sub = ""
        self.channel = 'test_channel'
        self.message = {
            'schema': 'http://schema.superbalist.com/events/user/created/1.0.json',
            'user': {
                'id': 1234,
                'first_name': 'Python',
                'last_name': 'Test',
                'email': 'python.test@example.org',
            },
            'date': '2017-02-10T18:25:43.511Z',
            'uuid': '0b5ed77a-4c9c-4c1a-8006-5d92ee88bb35',
            'service': 'test_service',
            'hostname': 'test_hostname',
        }

    def tearDown(self):
        if self.sub != "":
            self.sub.delete(self.channel)

    @pytest.mark.timeout(60)
    # @pytest.mark.parametrize('adapter', adapters_list)
    def test_event(self, adapter=GoogleCloudAdapter()):
        self.sub = adapter
        self.sub.add_topic(self.channel)
        self.sub.add_subscription(self.channel)
        gen = self.sub.subscribe(self.channel)
        self.pub = GoogleCloudAdapter()

        this = True
        messages = []
        while this:
            try:
                self.pub.publish(self.channel, self.message)
                messages = ast.literal_eval(next(gen))
                this = False
            except StopIteration:
                this = False
        assert self.message == messages
