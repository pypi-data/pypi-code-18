import re
import time
import json

import redis
import jsonschema
from google.cloud import pubsub
from google.cloud.exceptions import NotFound
from google.gax.errors import GaxError
from jsonschema import validate
from kafka import KafkaConsumer, KafkaProducer


class BasePubSubAdapter(object):
    """
    PubSub adapter base class
    """

    def __init__(self):
        pass

    def validate_message(self, message):
        if not message.get('schema', None):
            raise ValueError('Message must contain a schema!')
        schema_uri = message['schema']
        matches = re.findall(r'(.+)://(.+/)?events/(.+)/(.+)/(.+)\.json', schema_uri)[0]
        if matches:
            schema = jsonschema.RefResolver('', '').resolve_remote(schema_uri)
            validate(message, schema)
        else:
            raise ValueError('Incorrect schema uri')

    def publish(self, channel, message, **kwargs):
        raise NotImplementedError('Not implemented')

    def subscribe(self, channel, handler=lambda x: x, **kwargs):
        raise NotImplementedError('Not implemented')


class GoogleCloudAdapter(BasePubSubAdapter):
    """
    Google-cloud adapter class
    """

    def __init__(self):
        self.pubsub_client = pubsub.Client()
        self.client_identifier = None

    def publish(self, topic, message):
        topic = self.pubsub_client.topic(topic)
        if not topic.exists():
            topic.create()
        self.validate_message(json.loads(json.dumps(message)))
        try:
            topic.publish('{}'.format(message).encode())
        except GaxError:
            self.publish(topic.name, message)

    def subscribe(self, topic, handler=lambda x: x):
        topic = self.pubsub_client.topic(topic)
        subscription = self.subscription_name(topic)

        if not topic.exists():
            self.add_topic(topic.name)
        if not subscription.exists():
            self.add_subscription(topic.name)

        subscribed = True
        while subscribed:
            try:
                messages = subscription.pull()
            except GaxError:
                continue
            for ack_id, message in messages:
                yield handler(message.data.decode())
            if messages:
                subscription.acknowledge([ack_id for ack_id, message in messages])

    def set_client_identifier(self, identifier):
        self.client_identifier = identifier

    def subscription_name(self, topic):
        subscription_name = topic.name
        if self.client_identifier:
            subscription_name = '{}.{}'.format(self.client_identifier, topic.name)
        return topic.subscription(subscription_name)

    # Made add topic and add subscription so that tests could be made without threads.
    # this way we can create a topic and subscription and then publish instead of having
    # two thread(one creating the topic and the other waiting until it is created beofre
    # publishin gto it)

    # Also simplifis things because the GAX error catching only has to be done in one
    # place and not everywhere that it hapapens

    def delete(self, topic):
        try:
            self.delete_subscription(topic, topic)
            self.delete_topic(topic)
        except GaxError:
            self.remove(topic)

    def add_topic(self, topic):
        topic = self.pubsub_client.topic(topic)
        try:
            topic.create()
        except GaxError:
            self.add_topic(topic.name)

    def add_subscription(self, topic):
        topic = self.pubsub_client.topic(topic)
        subscription = self.subscription_name(topic)
        try:
            subscription.create()
        except GaxError:
            self.add_subscription(topic.name)

    def delete_topic(self, topic):
        topic = self.pubsub_client.topic(topic)
        try:
            topic.delete()
        except GaxError:
            self.delete_topic(topic.name)
        except Exception:
            raise NotFound('Topic not found')

    def delete_subscription(self, topic, subscription):
        topic = self.pubsub_client.topic(topic)
        subscription = topic.subscription(subscription)
        try:
            subscription.delete()
        except GaxError:
            self.delete_subscription(topic.name, subscription.name)
        except Exception:
            raise NotFound('Subscription not found')

    def get_topics(self):
        l = []
        try:
            for topic in self.pubsub_client.list_topics():
                l.append(topic.name)
        except GaxError:
            l = self.get_topics()
        return l

    def get_subscriptions(self, topic=None):
        l = []
        try:
            if topic:
                for subscription in self.pubsub_client.topic(topic).list_subscriptions():
                    l.append(subscription.name)
            else:
                for subscription in self.pubsub_client.list_subscriptions():
                    l.append(subscription.name)
        except GaxError:
            l = self.get_subscriptions(topic=topic)
        return l


class KafkaAdapter(BasePubSubAdapter):
    """
    Kafka adapter class
    """

    def __init__(self, bootstrap_servers='localhost',
                 group_id=str(int(time.time())),
                 auto_offset_reset='latest'):
        self.consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                                      group_id=group_id,
                                      auto_offset_reset=auto_offset_reset)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def publish(self, topic, message):
        self.producer.send(topic, b'{}'.format(message))
        self.producer.close()

    def subscribe(self, topic, handler=lambda x: x):
        subscribed = True
        self.consumer.subscribe(topic)
        while subscribed:
            for message in self.consumer:
                if message.value == 'unsubscribe':
                    subscribed = False
                    break
                yield handler(message.value)
        self.consumer.close()

    def get_subscribed(self):
        print(self.consumer.subscription())

    def get_topics(self):
        print(self.consumer.topics())


class RedisAdapter(BasePubSubAdapter):
    """
    Redis adapter class
    """

    def __init__(self, host='mobile-redis'):
        self.redis = redis.StrictRedis(host=host)
        self.pubsub = self.redis.pubsub()

    def publish(self, channel, message):
        self.redis.publish(channel, message)

    def subscribe(self, channel, handler=lambda x: x):
        self.subscribed = True
        self.pubsub.subscribe(channel)
        while self.subscribed:
            message = self.pubsub.get_message()
            if message:
                # Still need to test unsubscribe
                if message == 'unsubscribe':
                    self.subscribed = False
                    break
                yield handler(message['data'])
            time.sleep(0.5)
