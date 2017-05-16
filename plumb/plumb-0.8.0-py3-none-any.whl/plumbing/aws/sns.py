import logging
from . import SNSResource
from ..serializers import JSON


class Sink(SNSResource, JSON):
    """Uses the boto3 Topic object.

    Takes a topic object to put messages to it.

    Relies on create_topic() and topic.publish() as described in:
    http://boto3.readthedocs.org/en/latest/reference/services/sns.html#topic
    """

    #
    # TODO: use topic name for logging.
    #

    def __init__(self, topic=None, topic_name=None, sns=None):
        """Prepare the sink with a configured SNS backend.

        Either the SNS topic object or its name must be passed (topic object is
        preferred).

        Keyword parameters:
        * topic: the topic object.
        * topic_name: alternatively, the topic name.
        * sns: optionaly, a SNS handler to get the topic by name.
        """
        self.log = logging.getLogger('sns.sink')
        if topic is None:
            topic = self._get_topic(topic_name, sns)
        self.topic = topic
        self.log.debug('using SNS topic ARN="%s"' % self.topic.arn)

    def put(self, pkg):
        """Sends the raw package via the topic (to all transport protocols).

        Positional parameters:
        * the raw package dict.
        """
        msg = self.serialize(pkg)
        self.log.debug('sending to topic JSON encoded package: %s' % msg)
        self.topic.publish(Message=msg)
