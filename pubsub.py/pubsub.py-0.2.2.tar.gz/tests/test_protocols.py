from collections import defaultdict, deque
from unittest import TestCase

from jsonschema import ValidationError

from pubsub.protocol import Protocol
from pubsub.serializers.serializer import JSONSerializer
from pubsub.validators.validator import SchemaValidator


class MockGoogleAdapter(object):
    """
    PubSub adapter base class
    """

    def __init__(self, client_identifier):
        self.client_id = client_identifier
        self._messages = defaultdict(deque)

    def publish(self, channel, message):
        self._messages[channel].appendleft(message)

    def subscribe(self, channel):
        class MockMessage:
            def __init__(self, message):
                self.data = message
        r = MockMessage(self._messages[channel].pop())
        yield r


class ProtocolTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = Protocol(
            adapter=MockGoogleAdapter('test-client'),
            serializer=JSONSerializer(),
            validator=SchemaValidator())
        cls.valid_message = {
            "schema": "http://schema.superbalist.com/events/shopping_cart/created/1.0.json",
            "meta": {
                "date": "2017-02-01T12:39:12+00:00",
                "uuid": "5AB2ABB6-8617-4DDA-81F7-DD47D5882B19",
                "service": "api",
                "hostname": "superbalist-api-1935885982-59xk1"
            },
            "shopping_cart": {
                "id": 1070486,
                "is_expired": False,
                "is_restorable": True,
                "user": {
                    "id": 2,
                    "email": "matthew@superbalist.com",
                    "first_name": "Matthew",
                    "last_name": "Goslett"
                },
                "items": [

                ]
            }
        }
        cls.invalid_json_message = {'blah': 'blah'}
        cls.invalid_schema_uri = {
            "schema": "http://schema.superbalist.com/events/invalid/blahblah.json",
            "meta": {
                "date": "2017-02-01T12:39:12+00:00",
                "uuid": "5AB2ABB6-8617-4DDA-81F7-DD47D5882B19",
                "service": "api",
                "hostname": "superbalist-api-1935885982-59xk1"
            },
            "shopping_cart": {
                "id": 1070486,
                "is_expired": False,
                "is_restorable": True,
                "user": {
                    "id": 2,
                    "email": "matthew@superbalist.com",
                    "first_name": "Matthew",
                    "last_name": "Goslett"
                },
                "items": [

                ]
            }
        }
        cls.invalid_schema = {
            "schema": "http://schema.superbalist.com/events/shopping_cart/created/1.0.json",
            "meta": {
                "date": "2017-02-01T12:39:12+00:00",
                "uuid": "5AB2ABB6-8617-4DDA-81F7-DD47D5882B19",
                "service": "api",
                "hostname": "superbalist-api-1935885982-59xk1"
            },
            "shopping_cart": {
                "id": 1070486,
                "is_expired": False,
                "is_restorable": True,
                "user": {
                    "id": 2,
                    "email": "matthew@superbalist.com",
                    "first_name": "Matthew",
                    "last_name": "Goslett"
                }
            }
        }
        cls.invalid_message = 'hello world'

    @classmethod
    def tearDownClass(cls):
        pass

    def test_valid_message(self):
        self.protocol.publish('python_test', self.valid_message)
        sub = self.protocol.subscribe('python_test')
        for message in sub:
            assert message == self.valid_message

    def test_invalid_json_message(self):
        with self.assertRaises(KeyError):
            self.protocol.publish('python_test', self.invalid_json_message)

    def test_invalid_schema_uri(self):
        with self.assertRaises(ValidationError):
            self.protocol.publish('python_test', self.invalid_schema_uri)

    def test_invalid_schema(self):
        with self.assertRaises(ValidationError):
            self.protocol.publish('python_test', self.invalid_schema)

    def test_invalid_message(self):
        with self.assertRaises(TypeError):
            self.protocol.publish('python_test', self.invalid_message)


    # Only have one of these just to test its actually working
    # def test_real_google(self):
    #     protocol = Protocol(adapter=GooglePubsub(client_identifier='test_'), serializer=JSONSerializer(),
    #                         validator=SchemaValidator())
    #     protocol.publish('python_test', self.valid)
    #     sub = protocol.subscribe('python_test')
    #     for message in sub:
    #         assert message == self.valid
