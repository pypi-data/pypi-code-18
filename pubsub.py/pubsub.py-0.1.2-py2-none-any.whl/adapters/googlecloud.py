import json
from google.cloud import pubsub
from google.cloud.exceptions import NotFound
from google.gax.errors import GaxError
from pubsub.adapters.base import BaseAdapter
from pubsub.adapters.exceptions import IdentifierRequiredException, TopicNotFound


class GooglePubsub(BaseAdapter):
    """
    Google-cloud adapter class
    """

    def __init__(self):
        self.pubsub_client = pubsub.Client()
        self.client_identifier = None

    def publish(self, topic_name, message):
        topic = self.pubsub_client.topic(topic_name)
        if not topic.exists():
            topic.create()
        topic.publish(message.encode())

    def subscribe(self, topic_name, handler=lambda x: x):
        topic = self.pubsub_client.topic(topic_name)
        subscription = self.make_subscription(topic)

        if not topic.exists():
            raise TopicNotFound("Can't subscribe to unknown topic: {}".format(topic_name))
        if not subscription.exists():
            subscription.create()

        subscribed = True
        while subscribed:
            try:
                messages = subscription.pull()
            except GaxError:
                continue
            for ack_id, message in messages:
                yield handler(message.data.decode())
                subscription.acknowledge([ack_id])

    def set_client_identifier(self, identifier):
        self.client_identifier = identifier

    def make_subscription(self, topic):
        if self.client_identifier:
            subscription_name = '{}.{}'.format(self.client_identifier, topic.name)
        else:
            raise IdentifierRequiredException("Use obj.set_client_identifier('name')")
        return topic.subscription(subscription_name)

    def delete(self, topic):
         return self.delete_topic(topic)

    def delete_topic(self, topic):
        try:
            topic.delete()
        except Exception:
            raise TopicNotFound("Can't delete unknown topic".format(topic))

    def delete_subscription(self, subscription):
        try:
            subscription.delete()
        except Exception:
            raise NotFound('Subscription not found')
